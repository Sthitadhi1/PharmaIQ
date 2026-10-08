import { useCallback, useEffect, useState } from 'react';
import api, { getErrorMessage } from '../services/api';

type ApiData<T> = {
  data: T | null;
  loading: boolean;
  error: string | null;
  reload: () => void;
};

// GET an API path (relative to /api) and keep it in state; `reload` re-fetches live data.
function useApiData<T>(path: string): ApiData<T> {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [version, setVersion] = useState(0);

  useEffect(() => {
    let active = true;
    setLoading(true);
    api
      .get<T>(path)
      .then((response) => {
        if (active) {
          setData(response.data);
          setError(null);
        }
      })
      .catch((err) => {
        if (active) setError(getErrorMessage(err, 'Could not load data. Is the backend running on port 8000?'));
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, [path, version]);

  const reload = useCallback(() => setVersion((value) => value + 1), []);
  return { data, loading, error, reload };
}

export default useApiData;
