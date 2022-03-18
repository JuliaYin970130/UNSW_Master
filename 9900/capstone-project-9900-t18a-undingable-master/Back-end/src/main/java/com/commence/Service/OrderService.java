package com.commence.Service;

import com.commence.Utils.ReturnResult;
import com.commence.mbg.model.OrderInObj;

/**
 * @Program: capstone-project-9900-t18a-undingable
 * @Description:
 * @Date: 2021/11/7 15:16
 * @Auther: Jiahui Wang
 */
public interface OrderService {
    ReturnResult viewByProductId(Long product_id);

    ReturnResult viewById(Long order_id);

    ReturnResult view(Long user_id);

    ReturnResult checkout(OrderInObj order);
}
