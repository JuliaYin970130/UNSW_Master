package com.commence.Service;

import com.commence.Utils.ReturnResult;
import com.commence.mbg.model.User;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.List;

/**
 * @program: capstone-project-9900-t18a-undingable
 * @description: Abstract User service
 * @author: Jiahui Wang
 * @create: 2021-10-06 21:17
 **/
public interface UserService {

    ReturnResult queryList();
    ReturnResult login(User user, HttpServletResponse response);

    List<User> getUserByName(User user);

    ReturnResult Register(User user);

    ReturnResult updateProfile(User user);
}
