const fetcher = async <T>(
  url: string,
  method: string = "GET",
  body?: object,
  headers?: RequestInit["headers"]
): Promise<T> => {
  let storedValue = localStorage.getItem("USER_SESION");

  const requestInit: RequestInit = {
    method,
    headers: headers || {},
  };

  if (storedValue) {
    const token = JSON.parse(storedValue)?.access_token;
    if (typeof token === "string" && token.length) {
      requestInit.headers = {
        ...requestInit.headers,
        Authorization: `Bearer ${token}`,
      };
    }
  }

  if (body) {
    requestInit.headers = {
      "Content-Type": "application/json",
      ...requestInit.headers,
    };
    requestInit.body =
      // @ts-ignore-next-line
      requestInit.headers["Content-Type"] ===
      "application/x-www-form-urlencoded"
        ? new URLSearchParams(body as Record<string, string>)
        : JSON.stringify(body);
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
