import qs from 'querystring';
import { request, handleReturnResult } from './base';
// questionary api
export const viewShoppingCart = (userId) => request.get('/shoppingCart/view', {
	params: {
		id: userId
	}
}).then(handleReturnResult);

export const updateQuantity = (userId, productId, quantity) => request.post('/shoppingCart/quantity', qs.stringify({
	user_id: userId,
	quantity,
	product_id: productId
})).then(handleReturnResult);

export const addShoppingCart = (userId, productId, quantity) => request.post('/shoppingCart/add', qs.stringify({
	user_id: userId,
	quantity,
	product_id: productId
})).then(handleReturnResult);

export const deleteShoppingCart = (userId, productId) => request.post('/shoppingCart/delete', qs.stringify({
	user_id: userId,
	product_id: productId
})).then(handleReturnResult);
