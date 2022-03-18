import qs from 'querystring';
import { request, handleReturnResult } from './base';
//order api
export const queryOrderByProductId = (productId) => request.get('/order/viewByProductId', {
	params: {
		product_id: productId
	}
}).then(handleReturnResult);

export const queryOrderById = (orderId) => request.get('/order/viewById', {
	params: {
		order_id: orderId
	}
}).then(handleReturnResult);

export const queryOrderList = (userId) => request.get('/order/view', {
	params: {
		user_id: userId
	}
}).then(handleReturnResult);

export const checkout = (userId, products, amount) => request.post('/order/checkout', qs.stringify({
	userId,
	...products,
	amount
})).then(handleReturnResult);