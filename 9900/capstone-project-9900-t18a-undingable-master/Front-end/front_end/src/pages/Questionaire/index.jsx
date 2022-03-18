import React, { useState, useEffect } from 'react';
import {
    Link,
    useHistory
} from 'react-router-dom';
import { Button, Form, Typography, Radio, InputNumber, Space,Divider, Row, Col, Spin, message } from 'antd';
import { getQuestionaire, submitQuestionaire, updateQuestionaire } from '../../apis/user';
import { getUserInfo } from '../../utils';

import './index.css';

const { Title } = Typography;

const Questionaire = () => {
    const [isLoading, setIsLoading] = useState(false);
    const [questionaire, setQuestionaire] = useState({
        'price': {
            lower: 1,
            upper: 1000
        }
    });

	const history = useHistory();
    const onFinish = async (values) => {
        const userInfo = getUserInfo();
        if (!userInfo || !userInfo.id) {
            message.error('You must be logined!');
            return;
        }
        console.log('Questionaire values', values);
        try {
            const submitFn = questionaire.forwho ? updateQuestionaire : submitQuestionaire;
            await submitFn({
                userid: userInfo.id,
                family: values.family,
                forwho: values.forwho,
                brand: values.brand,
                lowerprice: values.price.lower,
                higherprice: values.price.upper
            });
            history.push('/');
        } catch (error) {
            message.error(`Error: ${error.message}`)
        }
    };

    useEffect(() => {
        const userInfo = getUserInfo();
        if (!userInfo) {
            history.push('/login');
            return;
        }
        setIsLoading(true);
        getQuestionaire(userInfo.id)
        .then((questionaire) => {
            if (questionaire) {
                setQuestionaire({
                    family: questionaire.family,
                    forwho: questionaire.forwho,
                    brand: questionaire.brand,
                    price: {
                        upper: questionaire.higherprice,
                        lower: questionaire.lowerprice
                    }
                });
            }
            setIsLoading(false);
        })
        .catch((err) => {
            message.error(err.message);
            setIsLoading(false);
        });
    }, [history]);

    if (isLoading) {
        return (
            <div id="quest-page">
                <Spin />
            </div>
        );
    }

    return (
        <div id="quest-page">
            <Title>Welcome to UD fragrance !</Title>
            <Title level={4}>Please fill the questionaire, then it will generate your stylish frangrance </Title>
            <Divider />
            <Form
                name="basic"
                layout="vertical"
                labelCol={{
                    span: 10,
                }}
                wrapperCol={{
                    span: 20,
                }}
                onFinish={onFinish}
                initialValues={questionaire}
                autoComplete="off"
                style={{
                    width: '100%',
                    marginTop: 20
                }}
            >
                <Form.Item
                    label="Who will use it?"
                    name="forwho"
                    rules={[
                        {
                            required: true,
                            message: 'This quesition is required!',
                        },
                    ]}
                >
                    <Radio.Group>
                        {/* <Radio value="you">you</Radio> */}
                        <Radio value="her">her</Radio>
                        <Radio value="him">him</Radio>
                    </Radio.Group>
                </Form.Item>

                <Form.Item
                    label="What frangrance family you would like?"
                    name="family"
                    rules={[
                        {
                            required: true,
                            message: 'This quesition is required!',
                        },
                    ]}
                >
                    <Radio.Group>
                        <Radio value="Floral">Floral</Radio>
                        <Radio value="Amber">Amber</Radio>
                        <Radio value="Woody">Woody</Radio>
                        <Radio value="Fresh">Fresh</Radio>
                        <Radio value="Fruity">Fruity</Radio>
                        <Radio value="Oriental">Oriental</Radio>
                        <Radio value="Rum">Rum</Radio>
                        <Radio value="Spice">Spice</Radio>
                    </Radio.Group>
                </Form.Item>

                <Form.Item
                    label="Which of the following brands do you like or are familiar with?"
                    name="brand"
                    rules={[
                        {
                            required: true,
                            message: 'This quesition is required!',
                        },
                    ]}
                >
                    <Radio.Group>
                        <Row>
                            <Col span={8}><Radio value="BVLGARI">BVLGARI</Radio></Col>
                            <Col span={8}><Radio value="Chanel">Chanel</Radio></Col>
                            <Col span={8}><Radio value="Creed">Creed</Radio></Col>
                            <Col span={8}><Radio value="Calvin Klein">Calvin Klein</Radio></Col>
                            <Col span={8}><Radio value="Gucci">Gucci</Radio></Col>
                            <Col span={8}><Radio value="Guerlain">Guerlain</Radio></Col>
                            <Col span={8}><Radio value="HERMAS">HERMAS</Radio></Col>
                            <Col span={8}><Radio value="Tom Ford">Tom Ford</Radio></Col>
                        </Row>
                    </Radio.Group>
                </Form.Item>
                <Form.Item
                    label="Your budget range is?"
                    required
                >
                    <Space>
                        <span>From</span>
                        <Form.Item
                            name={['price', 'lower']}
                            noStyle
                            rules={[{ required: true, message: 'This quesition is required!' }]}
                        >
                            <InputNumber />
                        </Form.Item>
                        <span>to</span>
                        <Form.Item
                            name={['price', 'upper']}
                            noStyle
                            rules={[{ required: true, message: 'This quesition is required!' }]}
                        >
                            <InputNumber />
                        </Form.Item>
                    </Space>
                </Form.Item>

                <Form.Item
                    wrapperCol={{
                        offset: 10,
                        span: 16,
                    }}
                >
                    <div id="quest-btn-wrapper">
                        <Button
                            type="primary"
                            htmlType="submit"
                        >
                            Submit
                        </Button>
                        <Link to="/" className="skip">
                            <Button type="link">Skip</Button>
                        </Link>
                    </div>
                </Form.Item>
            </Form>
        </div>
    );
}

export default Questionaire;
