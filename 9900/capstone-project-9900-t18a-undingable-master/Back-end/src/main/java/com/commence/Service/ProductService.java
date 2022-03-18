package com.commence.Service;

import com.commence.Utils.ReturnResult;
import com.commence.mbg.model.Product;
import com.commence.mbg.model.User;
import org.springframework.stereotype.Service;

/**
 * @program: capstone-project-9900-t18a-undingable
 * @description: Serivce for product
 * @author: Jiahui Wang
 * @create: 2021-10-27 17:07
 **/
public interface ProductService {
    ReturnResult view(Product product);

    ReturnResult viewByPriceRange(Integer low_price, Integer high_price);

    ReturnResult recommend(User user, int top_k);

    ReturnResult get_all_sale();
}
