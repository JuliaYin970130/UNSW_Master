import React, { Fragment } from "react";
import { Link, useHistory } from "react-router-dom";
import { getUserInfo } from "../../utils";
import { Layout, Menu, Dropdown, Button, Input, message } from "antd";
import { HomeOutlined, UserOutlined, ShoppingOutlined, TeamOutlined } from "@ant-design/icons";
import "./Header.css";

const { Search } = Input;
const { Header } = Layout;

const HeaderComp = () => {

    const userInfo = getUserInfo();
    const history = useHistory();

    const menu = (
        <Menu>
            {/* sign up */}
            {userInfo && userInfo.name ? (
                <Fragment>
                    <Menu.Item key="username">
                        <Link to="/user">
                            <Button type="text">{userInfo.name}</Button>
                        </Link>
                    </Menu.Item>
                    {userInfo.role <= 1
                        ? <Menu.Item key="admin-dashboard">
                            <Link to="/admin">
                                <Button type="text">Admin Dashboard</Button>
                            </Link>
                        </Menu.Item>
                        : null
                    }
                    {userInfo.role === 0
                        ? <Menu.Item key="admin-manage">
                            <Link to="/adminManage">
                                <Button type="text">Manage Admin</Button>
                            </Link>
                        </Menu.Item>
                        : null
                    }
                    <Menu.Item key="log-off">
                        <Button
                            onClick={() => {
                                const isConfirm = window.confirm("Do you want to logout?");
                                if (!isConfirm) {
                                    return;
                                }
                                // Logout
                                window.localStorage.removeItem("loginState");
                                // window.location.reload();
                                window.location = '/';
                            }}
                            type="text"
                        >
                            Logout
                        </Button>
                    </Menu.Item>
                </Fragment>
            ) : (
                <Fragment>
                    <Menu.Item key="sign-in">
                        <Link to="/login">
                            <Button type="text">Sign in</Button>
                        </Link>
                    </Menu.Item>
                    <Menu.Item key="sign-up">
                        <Link to="/reg">
                            <Button type="text">Register</Button>
                        </Link>
                    </Menu.Item>
                </Fragment>
            )}
        </Menu>
    );

    // search function
    const onSearch = (value) => {
        console.log(value);
        if (value) {
            // search content
            history.push(`/search?keyword=${value}`);
        } else message.error('Please check your search input!');
    }


    return (
        <Header
            style={{
                position: 'sticky',
                top: 0,
                backgroundColor: "#fff",
                zIndex: 999,
                width: "100vw",
                borderBottom: '1px solid #f0f0f0',
            }}
        >
            <Menu mode="horizontal" style={{ position: "relative" }} selectable={false}>
                {/* home page  */}
                <Menu.Item key="homepage" style={{ fontSize: "20px" }}>
                    <Link to="/">
                        <HomeOutlined style={{ fontSize: "20px", margin: "5px" }} />
                        Home
                    </Link>
                </Menu.Item>

                {/* cart */}
                <Menu.Item
                    key="Cart"
                    style={{ position: "absolute", right: "8%", fontSize: "16px" }}
                >
                    {/* <ShoppingOutlined /> */}
                    <Link to="Cart">
                        <ShoppingOutlined style={{ fontSize: "16px", marginRight: "5px" }} />
                        Cart
                    </Link>
                </Menu.Item>

                {/* Account content */}
                <Dropdown overlay={menu} placement="bottomCenter" >

                    <a
                        href="/#"
                        className="link"
                        onClick={(e) => e.preventDefault()}
                        style={{
                            position: "absolute",
                            right: 0,
                            fontSize: "16px",
                            color: "#000",
                        }}
                    >
                        <UserOutlined style={{ marginRight: '5px' }} />
                        Account
                    </a>
                </Dropdown>
            </Menu>
            <Search
                placeholder="Search"
                onSearch={onSearch}
                style={{
                    position: "relative",
                    left: "30%",
                    top: "-46px",
                    width: "400px",
                }}
                enterButton
            />
        </Header>
    );
};

export default HeaderComp;
