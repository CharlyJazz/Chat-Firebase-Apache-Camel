const fetcher = async (url: string) => {
  let storedValue = localStorage.getItem("USER_SESION");

  const requestInit: RequestInit = {};

  if (storedValue) {
    const token = JSON.parse(storedValue)?.access_token;
    if (typeof token === "string" && token.length) {
      requestInit.headers = {
        Authorization: `Bearer ${token}`,
      };
    }
  }

  const response = await fetch(url, requestInit);

  if (!response.ok) {
    const error = new Error("An error occurred while fetching the data.");
    // Attach extra info to the error object.
    error.message = await response.json();
    error.name = `Status ${response.status}`;
    throw error;
  }

  const data = await response.json();
  return data;
};

export { fetcher };
