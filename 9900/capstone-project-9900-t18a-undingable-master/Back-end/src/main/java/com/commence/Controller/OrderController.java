package com.commence.Controller;

import com.commence.Service.OrderService;
import com.commence.Utils.ReturnResult;
import com.commence.mbg.model.OrderInObj;
import com.commence.mbg.model.Product;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;

import java.util.List;

/**
 * @Program: capstone-project-9900-t18a-undingable
 * @Description: Controller for order function
 * @Date: 2021/11/7 15:16
 * @Auther: Jiahui Wang
 */
@CrossOrigin(origins = "*")
@Controller
@RequestMapping("/order")
public class OrderController {

    @Autowired
    private OrderService orderService;

    @RequestMapping(value = "/viewById", method = RequestMethod.GET)
    @ResponseBody
    public ReturnResult viewById(Long order_id){
        return orderService.viewById(order_id);
    }

    @RequestMapping(value = "/viewByProductId", method = RequestMethod.GET)
    @ResponseBody
    public ReturnResult viewByProductId(Long product_id){
        return orderService.viewByProductId(product_id);
    }


    @RequestMapping(value = "/view", method = RequestMethod.GET)
    @ResponseBody
    public ReturnResult view(Long user_id){
        return orderService.view(user_id);
    }

    @RequestMapping(value = "/checkout", method = RequestMethod.POST)
    @ResponseBody
    public ReturnResult checkout(OrderInObj order){
        return orderService.checkout(order);
    }
}
