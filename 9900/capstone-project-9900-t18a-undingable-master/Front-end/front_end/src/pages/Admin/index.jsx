import React, { useState, useEffect } from 'react';
import { Layout, Divider, Table, Button, Modal, Form, Input, Radio, Select, message } from 'antd';
import { DeleteOutlined }  from '@ant-design/icons';
import { Link } from 'react-router-dom';
import { queryItems } from '../../apis/product';
import { queryUserList } from '../../apis/user';

import './index.css';

const Admin = () => {
    const { Content } = Layout;
    const { Option } = Select;

    const [dataSource, setDataSource] = useState([]);
    const [userList, setUserList] = useState([]);

    useEffect(() => {
        queryItems({}, true)
            .then((itemList) => {
                setDataSource(itemList.map((item) => ({
                    ...item,
                    key: `item-${item.id}`
                })));
            })
            .catch((err) => {
                message.error(`[GetItemList Failed] ${err.message}`);
            });
    }, []);

    useEffect(() => {
        queryUserList()
            .then((userList) => {
                setUserList(userList.map((user) => ({
                    ...user,
                    key: `user-${user.id}`
                })));
            })
            .catch((err) => {
                message.error(`[GetUserList Failed] ${err.message}`);
            });
    }, []);

    const formItemLayout = {
        labelCol: {
            span: 6,
        },
        wrapperCol: {
            span: 14,
        },
    };

    // item表头
    const itemscolumns = [
        {
            title: "Item ID",
            dataIndex: "id",
            key: "id",
            render: (id) => 
                <Link to={`/itemManage?id=${id}`}>
                    {id}
                </Link>
        },
        {
            title: "Item Name",
            dataIndex: "name",
            key: "name",
        },
        {
            title: "Brand",
            dataIndex: "brand",
            key: "brand",
        },
        {
            title: "Stock",
            dataIndex: "stock",
            key: "stock",
        },
        {
            title: "Sales",
            dataIndex: "saleNum",
            key: "saleNum",
        },
        {
            title: "Action",
            key: "action",
            render: (record) => (
                // <a href="/#" >Delete</a>
                <DeleteOutlined onClick={()=>{onDeletRecord(record)}} style={{marginLeft:"30%"}}/>
                    
            )
        }
    ];

    const onDeletRecord = (record) =>{
        // console.log(record)
        setDataSource(pre => {
            return pre.filter(item => item.key !== record.key)
        })

    }

    // Add item relpy
    const [isModalVisible, setIsModalVisible] = useState(false);

    const showModal = () => {
        setIsModalVisible(true);
    };


    const onCreate = (values) => {
        console.log('Received values of form: ', values);
        const newRecord = {
            key: dataSource.length + 1,
            itemID: 56332998,
            itemName: values.itemName,
            Brand: values.brand,
            Stock: values.stock,
            Sales: 0,
        }

        setDataSource(pre=>{
            return [...pre,newRecord]
        })
        
        setIsModalVisible(false);
    };

    const handleCancel = () => {
        setIsModalVisible(false);
    };

    const [form] = Form.useForm();

    // 用户表头
    const userColumns = [
        {
            title: "User ID",
            dataIndex: "id",
            key: "id",
        },
        {
            title: "User Name",
            dataIndex: "name",
            key: "name",
        },
        {
            title: "Email",
            dataIndex: "email",
            key: "email",
        },
        {
            title: "Phone",
            dataIndex: "phone",
            key: "phone",
        },
    ];

    return (
        <Content
            className="AdminContainer"
            style={{ padding: "0 50px", minHeight: '95vh' }}
        >
            {/* 商品列表 */}
            <div className="item-list">
                {/* item信息 */}
                <h2>Item List</h2>
                {/* list */}
                <Divider></Divider>
                <Table
                    // 表头
                    columns={itemscolumns}
                    // 数据
                    dataSource={dataSource}
                    size="middle"
                    pagination={{ pageSize: 10, size: "small" }}
                />

                <Button type="primary" onClick={showModal}>
                    Add a new item
                </Button>

                <Modal
                    title="Add a new item"
                    visible={isModalVisible}
                    style={{ top: 60 }}
                    onCancel={handleCancel}
                    okText="Confirm"
                    onOk={() => {
                        form.validateFields()
                            .then((values) => {
                                form.resetFields();
                                onCreate(values);
                            })
                            .catch((err) => {
                                console.error(err);
                                message.error((err && err.message) || 'Unknown error');
                            });
                    }}
                >
                    {/* 添加商品的表单内容 */}
                    <Form
                        form={form}
                        // layout="vertical"
                        name="add_item"
                        {...formItemLayout}
                    >
                        <Form.Item
                            name="itemName"
                            label="Item name"
                            rules={[
                                {
                                    required: true,
                                    message: "Please input item name!",
                                },
                            ]}
                        >
                            <Input type="textarea" />
                        </Form.Item>
                        <Form.Item name="brand" label="Brand" rules={[
                            {
                                required: true,
                                message: 'Please input brand!',
                            },
                        ]}>
                            <Input type="textarea" />
                        </Form.Item>
                        <Form.Item name="gender" label="Gender" rules={[
                            {
                                required: true,
                                message: 'Please select gender!',
                            },
                        ]}>
                            <Radio.Group>
                                <Radio value="women">Women</Radio>
                                <Radio value="men">Men</Radio>
                                <Radio value="unisex">Unisex</Radio>
                            </Radio.Group>
                        </Form.Item>

                        <Form.Item
                            name="scentNotes"
                            label="Scent Notes"
                            rules={[
                                {
                                    required: true,
                                    message: 'Please select item scent notes!',
                                },
                            ]}
                        >
                            <Select>
                                <Option value="Amber">Amber</Option>
                                <Option value="Citrus">Citrus</Option>
                                <Option value="Floral">Floral</Option>
                                <Option value="Fresh">Fresh</Option>
                                <Option value="Fruity">Fruity</Option>
                                <Option value="Oriental">Oriental</Option>
                                <Option value="Rum">Rum</Option>
                                <Option value="Spice">Spice</Option>
                                <Option value="Woody">Woody</Option>
                            </Select>
                        </Form.Item>
                        <Form.Item name="price" label="Price"
                            rules={[
                                {
                                    required: true,
                                    message: 'Please input price!',
                                },
                            ]}>
                            <Input type="textarea" />
                        </Form.Item>
                        <Form.Item name="size" label="Size" rules={[
                            {
                                required: true,
                                message: 'Please input size!',
                            },
                        ]}>
                            <Input type="textarea" />
                        </Form.Item>
                        <Form.Item name="imgUrl" label="Image Url" rules={[
                            {
                                required: true,
                                message: 'Please input Image Url!',
                            },
                        ]}>
                            <Input type="textarea" />
                        </Form.Item>
                        <Form.Item name="stock" label="Stock" rules={[
                            {
                                required: true,
                                message: 'Please input stock!',
                            },
                        ]}>
                            <Input type="textarea" />
                        </Form.Item>
                        <Form.Item name="description" label="Description" rules={[
                            {
                                required: true,
                                message: 'Please input Description!',
                            },
                        ]}>
                            <Input.TextArea />
                        </Form.Item>
                    </Form>
                </Modal>
            </div>

            {/* 用户列表 */}
            <div className="user-list">
                {/* user信息 */}
                <h2>User List</h2>
                {/* list */}

                <Divider></Divider>
                <Table
                    // 表头
                    columns={userColumns}
                    // 数据
                    dataSource={userList}
                    size="middle"
                    pagination={{ pageSize: 10, size: "small" }}
                />
            </div>
        </Content>
    );
};
export default Admin;
