package com.commence.Service.Impl;

import com.commence.Service.UserService;
import com.commence.Utils.ReturnResult;
import com.commence.mbg.mapper.UserMapper;
import com.commence.mbg.model.User;
import com.commence.mbg.model.UserExample;
import lombok.extern.slf4j.Slf4j;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.util.DigestUtils;

import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletResponse;
import java.nio.charset.StandardCharsets;
import java.util.List;

/**
 * @program: capstone-project-9900-t18a-undingable
 * @description:
 * @author: Jiahui Wang
 * @create: 2021-10-06 21:18
 **/
@Service
@Slf4j
public class UserServiceImpl implements UserService {

    @Autowired
    private UserMapper userMapper;

    @Override
    public ReturnResult queryList() {
        List<User> userList = userMapper.selectByExample(new UserExample());
        for (User user : userList) {
            user.setPassword(null);
        }
        return ReturnResult.success(userList, "Return successfully");
    }

    @Override
    public ReturnResult login(User user, HttpServletResponse response) {

        if (user.getName() == null || user.getPassword() == null){
            return ReturnResult.failed(504, null, "No username or password");
        }
        List<User> userList = getUserByName(user);
        if (userList.size() > 0){
            User curr_user = userList.get(0);
            // Check with MD5 encoded password
            if ( DigestUtils.md5DigestAsHex(user.getPassword().getBytes(StandardCharsets.UTF_8)).equals(curr_user.getPassword())) {
                // If user login in, would send a Islogin to font-end
                // This is for long-life check
                Cookie cookie = new Cookie("IsLogin", "yes");
                cookie.setMaxAge(30);
                cookie.setPath("/");
                response.addCookie(cookie);
                // log.info("info");
                curr_user.setPassword(null);
                return ReturnResult.success(curr_user, "Return successfully");
            }
        }


        // If no password or username, then would return failure
        // instead of send 500 to user
        return ReturnResult.failed(504, null, "please input correct username or password");
    }

    @Override
    public List <User> getUserByName(User user) {
        System.out.println(user);
        String name = user.getName();
        UserExample userExample = new UserExample();
        userExample.createCriteria().andNameEqualTo(name);
        return userMapper.selectByExample(userExample);
    }

    @Override
    public ReturnResult Register(User user) {
        if (user.getName() == null || user.getPassword() == null){
            return ReturnResult.failed(504, null, "No username or password");
        }
        List<User> userList = getUserByName(user);
        if (userList.size() == 0){
            user.setPassword(DigestUtils.md5DigestAsHex(user.getPassword().getBytes(StandardCharsets.UTF_8)));
            int res = userMapper.insert(user);
            if (res == 1){
                user.setPassword(null);
                return ReturnResult.success(user, "register successfully");
            }
        }
        return ReturnResult.failed(505, null, "register failed because of username already exist");
    }

    @Override
    public ReturnResult updateProfile(User user) {
        if (user.getId() == null){
            return ReturnResult.failed(500, null, "No userId");
        }
        UserExample example = new UserExample();
        example.createCriteria().andIdEqualTo(user.getId());

        if (userMapper.updateByExampleSelective(user, example) == 1){
            return ReturnResult.success(user, "Update user successfully!");
        } else {
            return ReturnResult.failed(503, null, "Update user failed!");
        }
    }


}
