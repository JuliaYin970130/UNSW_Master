import { request, handleReturnResult } from './base';
import { getUserInfo } from '../utils';
// product api, use map to apply database
let _saleNumMap = new Map();
const getSaleNumMap = async () => {
    if (!_saleNumMap.size) {
        const saleNumResponse = await request.get('/product/Sale');
        const saleNumList = handleReturnResult(saleNumResponse);
        for (const { productid, salenum } of saleNumList) {
            _saleNumMap.set(productid, salenum);
        }
    }
    return _saleNumMap;
};

export const queryItems = async (query, disableRecommend) => {
    let itemsResponse;
    if (query && query.price) {
        const [lowPrice, highPrice] = query.price.split(':');
        itemsResponse = await request.get('/product/viewByPriceRange', {
            params: {
                low_price: lowPrice * 100,
                high_price: highPrice * 100
            }
        });
    } else if (!disableRecommend && (!query || !Object.entries(query).length)) {
        const userInfo = await getUserInfo();
        itemsResponse = await request.get('/product/recommend', {
            params: {
                id: (userInfo && userInfo.id) || 0,
                top_k: 50
            }
        });
    } else {
        itemsResponse = await request.get('/product/view', { params: query });
    }
    const itemList = await handleReturnResult(itemsResponse);
    const saleNumMap = await getSaleNumMap();
    return itemList.map((item) => ({
        ...item,
        saleNum: saleNumMap.get(item.id)
    }));
};