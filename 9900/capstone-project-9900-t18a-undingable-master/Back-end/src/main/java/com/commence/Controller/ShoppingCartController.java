package com.commence.Controller;

import com.commence.Service.ShoppingCartService;
import com.commence.Utils.ReturnResult;
import com.commence.mbg.model.Product;
import com.commence.mbg.model.User;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;

/**
 * @Program: capstone-project-9900-t18a-undingable
 * @Description:
 * @Date: 2021/11/6 15:15
 * @Auther: Jiahui Wang
 */

@CrossOrigin(origins = "*")
@Controller
@RequestMapping("/shoppingCart")
public class ShoppingCartController {

    @Autowired
    private ShoppingCartService shoppingCartService;

    @RequestMapping(value = "/view", method = RequestMethod.GET)
    @ResponseBody
    public ReturnResult view(User user){
        return shoppingCartService.view(user);
    }

    @RequestMapping(value = "/add", method = RequestMethod.POST)
    @ResponseBody
    public ReturnResult add(Long product_id, Long quantity, Long user_id){
        return shoppingCartService.add(product_id, quantity, user_id);
    }

    @RequestMapping(value = "/delete", method = RequestMethod.POST)
    @ResponseBody
    public ReturnResult delete(Long product_id, Long user_id){
        return shoppingCartService.delete(product_id, user_id);
    }

    @RequestMapping(value = "/quantity", method = RequestMethod.POST)
    @ResponseBody
    public ReturnResult updateQuantity(Long product_id, Long quantity, Long user_id){
        return shoppingCartService.updateQuantity(product_id, quantity, user_id);
    }


}
