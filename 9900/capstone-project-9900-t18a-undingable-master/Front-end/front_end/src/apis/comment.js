import qs from 'querystring';
import { request, handleReturnResult } from './base';

export const viewCommentByProductId = (productId) => request.get('/comment/viewByProduct', {
	params: {
		product_id: productId
	}
}).then(handleReturnResult);

export const addOrUpdateComment = (orderId, productId, stars, comment) => request.post('/comment/addOrUpdate', qs.stringify({
	order_id: orderId,
	product_id: productId,
	stars,
	comment
})).then(handleReturnResult);