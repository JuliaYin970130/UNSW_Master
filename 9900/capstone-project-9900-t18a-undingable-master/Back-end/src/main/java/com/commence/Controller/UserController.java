package com.commence.Controller;

import com.commence.Service.UserService;
import com.commence.Utils.ReturnResult;
import com.commence.mbg.model.User;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * @program: capstone-project-9900-t18a-undingable
 * @description: Controller for user inferface
 * @author: Jiahui Wang
 * @create: 2021-10-06 21:14
 **/
@CrossOrigin(origins = "*")
@Controller
@RequestMapping("/user")
public class UserController {

    @Autowired
    private UserService userService;

    @RequestMapping(value = "queryList", method = RequestMethod.GET)
    @ResponseBody
    public ReturnResult queryList(){
        return userService.queryList();
    }

    @RequestMapping(value = "login", method = RequestMethod.POST)
    @ResponseBody
    public ReturnResult login(User user, HttpServletResponse response){
        return userService.login(user, response);
    }

    @RequestMapping(value = "register", method = RequestMethod.POST)
    @ResponseBody
    public ReturnResult register(User user){
        return userService.Register(user);
    }

    @RequestMapping(value = "updateProfile", method = RequestMethod.POST)
    @ResponseBody
    public ReturnResult updateProfile(User user){
        return userService.updateProfile(user);
    }

}
