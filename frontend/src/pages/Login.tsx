import { useState } from 'react';
import ApiResultPanel from '../components/ApiResultPanel';
import FormField from '../components/FormField';
import TestFormCard, { buttonClass, secondaryButtonClass } from '../components/TestFormCard';
import { callApi, type ApiResult } from '../services/api';

const shorten = (token: string) => `${token.slice(0, 18)}…${token.slice(-8)}`;

function Login() {
  const [username, setUsername] = useState('admin');
  const [password, setPassword] = useState('');
  const [accessToken, setAccessToken] = useState('');
  const [refreshToken, setRefreshToken] = useState('');
  const [oldRefreshToken, setOldRefreshToken] = useState('');
  const [loginResult, setLoginResult] = useState<ApiResult | null>(null);
  const [tokenResult, setTokenResult] = useState<ApiResult | null>(null);

  const login = async () => {
    const result = await callApi('post', '/auth/token', { username, password });
    setLoginResult(result);
    if (result.ok) {
      setAccessToken(result.data.access_token);
      setRefreshToken(result.data.refresh_token);
      setOldRefreshToken('');
    }
  };

  const whoAmI = async (withToken: boolean) => {
    const headers: Record<string, string> = withToken && accessToken ? { Authorization: `Bearer ${accessToken}` } : {};
    setTokenResult(await callApi('get', '/auth/me', undefined, headers));
  };

  const refresh = async () => {
    const result = await callApi('post', '/auth/refresh', { refresh_token: refreshToken });
    setTokenResult(result);
    if (result.ok) {
      setOldRefreshToken(refreshToken);
      setRefreshToken(result.data.refresh_token);
      setAccessToken(result.data.access_token);
    }
  };

  const replayOldToken = async () => {
    setTokenResult(await callApi('post', '/auth/refresh', { refresh_token: oldRefreshToken }));
  };

  return (
    <div className="space-y-8">
      <header>
        <p className="text-sm uppercase tracking-[0.3em] text-slate-500">Security</p>
        <h1 className="mt-3 text-3xl font-semibold text-slate-900">Login and tokens</h1>
      </header>

      <TestFormCard
        title="Log in"
        testCases="TC-02 · TC-03"
        hint="Demo accounts: admin / AdminPass123!, data_scientist / DataScience123!, business_user / Business123!. A wrong password must return 401."
      >
        <div className="grid gap-6 lg:grid-cols-2">
          <div className="space-y-4">
            <div className="grid gap-3 sm:grid-cols-2">
              <FormField label="Username" type="text" value={username} onChange={setUsername} />
              <FormField label="Password" type="password" value={password} onChange={setPassword} />
            </div>
            <button className={buttonClass} onClick={login}>Log in</button>
          </div>
          <ApiResultPanel result={loginResult} />
        </div>
      </TestFormCard>

      <TestFormCard
        title="Use the tokens"
        testCases="TC-04 · TC-15"
        hint="TC-04: “Who am I” without a token must give 401, with a token 200. TC-15: refresh once (200), then replay the old refresh token (must give 401)."
      >
        <div className="grid gap-6 lg:grid-cols-2">
          <div className="space-y-4">
            <dl className="space-y-1 font-mono text-xs text-slate-600">
              <div>access token: {accessToken ? shorten(accessToken) : '— log in first —'}</div>
              <div>refresh token: {refreshToken ? shorten(refreshToken) : '—'}</div>
              <div>old refresh token: {oldRefreshToken ? shorten(oldRefreshToken) : '— refresh once to create —'}</div>
            </dl>
            <div className="flex flex-wrap gap-3">
              <button className={secondaryButtonClass} onClick={() => whoAmI(false)}>Who am I (no token)</button>
              <button className={buttonClass} disabled={!accessToken} onClick={() => whoAmI(true)}>Who am I (with token)</button>
              <button className={buttonClass} disabled={!refreshToken} onClick={refresh}>Refresh token</button>
              <button className={secondaryButtonClass} disabled={!oldRefreshToken} onClick={replayOldToken}>Replay old refresh token</button>
            </div>
          </div>
          <ApiResultPanel result={tokenResult} />
        </div>
      </TestFormCard>
    </div>
  );
}

export default Login;
