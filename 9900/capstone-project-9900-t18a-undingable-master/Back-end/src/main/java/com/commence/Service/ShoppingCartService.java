package com.commence.Service;

import com.commence.Utils.ReturnResult;
import com.commence.mbg.model.User;

/**
 * @Program: capstone-project-9900-t18a-undingable
 * @Description:
 * @Date: 2021/11/6 15:15
 * @Auther: Jiahui Wang
 */
public interface ShoppingCartService {

    ReturnResult view(User user);

    ReturnResult add(Long product_id, Long quantity, Long user_id);

    ReturnResult delete(Long product_id, Long user_id);

    ReturnResult updateQuantity(Long product_id, Long quantity, Long user_id);
}
