import qs from 'querystring';
import { request, handleReturnResult } from './base';
// set different api and match the unique id info
export const queryUserList = () => request.get('/user/queryList').then(handleReturnResult);
export const login = (user) => request.post('/user/login', qs.stringify(user)).then(handleReturnResult);
export const register = (user) => request.post('/user/register', qs.stringify(user)).then(handleReturnResult);
export const updateProfile = (user) => request.post('/user/updateProfile', qs.stringify(user)).then(handleReturnResult);
export const getQuestionaire = (userId) => request.get('/questionnaire/get', {
	params: {
		userid: userId
	}
}).then(handleReturnResult).then((questionaireArr) => (Array.isArray(questionaireArr) && questionaireArr[0]) || null);
export const submitQuestionaire = (questionaire) => request.post('/questionnaire/insert', qs.stringify(questionaire)).then(handleReturnResult);
export const updateQuestionaire = (questionaire) => request.post('/questionnaire/update', qs.stringify(questionaire)).then(handleReturnResult);