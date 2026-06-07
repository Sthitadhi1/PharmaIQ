import { useState, useEffect } from 'react';

type FetchState<T> = {
  data: T | null;
  loading: boolean;
  error: string | null;
};

function useFetch<T>(fetcher: () => Promise<T>) {
  const [state, setState] = useState<FetchState<T>>({ data: null, loading: true, error: null });

  useEffect(() => {
    let mounted = true;

    fetcher()
      .then((data) => {
        if (mounted) setState({ data, loading: false, error: null });
      })
      .catch((error) => {
        if (mounted) setState({ data: null, loading: false, error: String(error) });
      });

    return () => {
      mounted = false;
    };
  }, [fetcher]);

  return state;
}

export default useFetch;
