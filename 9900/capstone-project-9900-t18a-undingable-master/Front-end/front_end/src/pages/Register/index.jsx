import React from 'react';
import {
    Link,
    useHistory
} from 'react-router-dom';
import { Layout, Button, Card, Form, Input, message } from 'antd';
import { register } from '../../apis/user';

import './index.css';
import { setUserInfo } from '../../utils';

const Register = () => {
	const history = useHistory();
    const onFinish = (values) => {
        const { username, email, password, confirmPassword } = values;
		if (password !== confirmPassword) {
			message.error('password and confirm-password is not same!');
			return;
		}
        return register({
            name: username,
            email,
            password,
            role:2
        })
        .then((res) => {
            setUserInfo(res);
            history.push('/questionaire');
        })
        .catch((err) => {
            console.error(err);
            message.error((err && err.message) || 'Unknown error');
        });
    };

    return (
        <Layout>
            <div id="reg-page">
                <Card id="reg-box" title="Register">
                    <div id="reg-box-body">
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
                            style={{
                                width: '100%'
                            }}
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
                                label="E-Mail"
                                name="email"
                                rules={[
                                    {
                                        required: true,
                                        message: 'Please input your e-mail!',
                                    },
                                ]}
                            >
                                <Input type="email" />
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
                                label="Confirm Password"
                                name="confirmPassword"
                                rules={[
                                    {
                                        required: true,
                                        message: 'Please input your confirm password!',
                                    },
                                ]}
                            >
                                <Input.Password />
                            </Form.Item>

                            <Form.Item
                                wrapperCol={{
                                    offset: 8,
                                    span: 16,
                                }}
                            >
                                <Button
                                    id="login-button"
                                    type="primary"
                                    htmlType="submit"
                                >
                                    Submit
                                </Button>
                            </Form.Item>
                        </Form>
                    </div>
                </Card>
                <div className="reg-bottom">
                    <Link to="/">
                        <div className="reg-bottom-btn">Skip and Visit</div>
                    </Link>
                </div>
            </div>
        </Layout>
    );
}
export default Register;
