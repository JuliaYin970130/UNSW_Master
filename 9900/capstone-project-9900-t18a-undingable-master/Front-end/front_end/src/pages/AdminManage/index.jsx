import React, { useState, useEffect } from 'react'
import { Layout, Card, Form, Input, Button,Table,message } from "antd";
import { DeleteOutlined}  from '@ant-design/icons';
import { queryUserList, register } from '../../apis/user';
import "./index.css";


const AdminManage = () => {

    const { Content } = Layout;

    const [adminDataSource, setAdminDataSource] = useState([]);

    const onFinish = (values) => {
        console.log(values)
        const { adminname, email, password, confirmPassword } = values;

        if (password !== confirmPassword) {
			message.error('password and confirm-password is not same!');
			return;
		}
        // add form


        return register({
            name: adminname,
            email,
            password,
            role:1
        })
        .then((res) => {
            // setUserInfo(res);
            const newRecord = {
                key: adminDataSource.length + 1,
                adminID: 56332998,
                adminName: values.adminname,
                email: values.email,
            }
    
            setAdminDataSource(pre=>{
                return [...pre,newRecord]
            })
        })
        .catch((err) => {
            console.error(err);
            message.error((err && err.message) || 'Unknown error');
        });
        
    }

    const admincolumns = [
        {
            title: "Admin ID",
            dataIndex: "id",
            key: "id",
        },
        {
            title: "Admin Name",
            dataIndex: "name",
            key: "name",
        },
        {
            title: "Email",
            dataIndex: "email",
            key: "email",
        },
        {
            title: "Action",
            key: "action",
            render: (record) => (
                <DeleteOutlined onClick={()=>{onDeleteRecord(record)}} style={{marginLeft:"30%"}}/>
            )
        }
    ];
    const onDeleteRecord = (record) =>{
        setAdminDataSource(pre => {
            return pre.filter(item => item.key !== record.key)
        })
    };

    useEffect(() => {
        queryUserList()
            .then((userList) => {
                setAdminDataSource(userList.map((user) => ({
                    ...user,
                    key: `user-${user.id}`
                })).filter((user) => user.role <= 1));
            })
            .catch((err) => {
                message.error(err.message);
            });
    }, []);

    return (
        <Content style={{ padding: '0 50px', minHeight: "95vh" }}>
            <div className="admin-container">
                {/* add new admin */}
                <div className="add-admin">
                    <Card title="Add a New Admin">

                        <Form
                            name="basic"
                            labelCol={{
                                span: 8,
                            }}
                            wrapperCol={{
                                span: 14,
                            }}
                            onFinish={onFinish}
                        >
                            <Form.Item
                                label="Admin Name"
                                name="adminname"
                                rules={[
                                    {
                                        required: true,
                                        message: 'Please input username!',
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
                                        message: 'Please input password!',
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
                                    offset: 6,
                                    span: 14,
                                }}
                            >
                                <Button
                                    id="login-button"
                                    type="primary"
                                    htmlType="submit"
                                >
                                    Add
                                </Button>
                            </Form.Item>

                        </Form>
                    </Card>

                </div>

                <div className="delete-admin">
                    <h2>Admin List</h2>
                    <Table
                        // header
                        columns={admincolumns}
                        // data
                        dataSource={adminDataSource}
                        size="middle"
                        pagination={{ pageSize: 10, size: "small" }}
                        id = "admin-table"
                    />
                </div>
            </div>
        </Content>
    )

}

export default AdminManage;