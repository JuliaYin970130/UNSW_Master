import qs from 'querystring';
import { request, handleReturnResult } from './base';
// json convert to stringify
export const login = (user) => request.post('/user/login', qs.stringify(user)).then(handleReturnResult);
