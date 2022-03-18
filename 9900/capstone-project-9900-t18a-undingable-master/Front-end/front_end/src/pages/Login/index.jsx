import React from 'react';
import {
    Link,
    useHistory
} from 'react-router-dom';
import { login } from '../../apis/user';
import { Button, Card, Form, Input, Checkbox, message } from 'antd';

import './index.css';
import { setUserInfo } from '../../utils';

const Login = () => {
    const history = useHistory();
    const onFinish = (values) => {
        const { username, password } = values;

        return login({
            name: username,
            password,
            role: 2
        })
        .then((res) => {
            setUserInfo(res);
            history.push('/');
        })
        .catch((err) => {
            console.error(err);
            message.error((err && err.message) || 'Unknown error');
        });
    };

    return (
        <div id="login-page">
            <Card id="login-box" title="Log In">
                <div id="login-box-body">
                    <Form
                        name="basic"
                        labelCol={{
                            span: 8,
                        }}
                        wrapperCol={{
                            span: 16,
                        }}
                        initialValues={{
                            remember: true,
                        }}
                        onFinish={onFinish}
                        autoComplete="off"
                    >
                        <Form.Item
                            label="Username"
                            name="username"
                            rules={[
                                {
                                    required: true,
                                    message: 'Please input your username!',
                                },
                            ]}
                        >
                            <Input />
                        </Form.Item>

                        <Form.Item
                            label="Password"
                            name="password"
                            rules={[
                                {
                                    required: true,
                                    message: 'Please input your password!',
                                },
                            ]}
                        >
                            <Input.Password />
                        </Form.Item>

                        <Form.Item
                            name="remember"
                            valuePropName="checked"
                            wrapperCol={{
                                offset: 8,
                                span: 16,
                            }}
                        >
                            <Checkbox>Remember me</Checkbox>
                        </Form.Item>

                        <Form.Item
                            wrapperCol={{
                                offset: 8,
                                span: 16,
                            }}
                        >
                            <div id="login-btn-wrapper">
                                <Button
                                    id="login-button"
                                    type="primary"
                                    htmlType="submit"
                                >
                                    Log In
                                </Button>
                                <Link to="/" className="skip">
                                    <Button>Back</Button>
                                </Link>
                            </div>
                        </Form.Item>

                        <Form.Item
                            wrapperCol={{
                                offset: 8,
                                span: 16,
                            }}
                            style={{
                                marginBottom: 0
                            }}
                        >
                            {/* <Link to="/reg">
                                <a href="">Forgot password?</a>
                            </Link> */}
                            <Link to="/reg" id="login-reg-link">
                                <Button type="link">New! Register Here!</Button>
                            </Link>
                        </Form.Item>
                    </Form>
                </div>
            </Card>
        </div>
    );
}

export default Login;
