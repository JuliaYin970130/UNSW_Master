import React, { useState, useEffect, Fragment } from 'react';
import { useLocation } from 'react-router-dom';
import { Layout, Space, Menu, Breadcrumb, message } from 'antd';

import Item from '../../components/Item';
import { queryItems } from '../../apis/product';

import './index.css';

const { SubMenu } = Menu;
const { Content, Sider } = Layout;

const CATEGORY = [
  {
    key: 'gender',
    title: 'Gender',
    valueMap: {
      'Women': 'Women',
      'Men': 'Men',
      'Unisex': 'Unisex'
    }
  },
  {
    key: 'brand',
    title: 'Top Brand',
    valueMap: {
      'BVLGARI': 'BVLGARI',
      'Chanel': 'Chanel',
      'Creed': 'Creed',
      'Calvin Klein': 'Calvin Klein',
      'Dior': 'Dior',
      'Gucci': 'Gucci',
      'Guerlain': 'Guerlain',
      'HERMAS': 'HERMAS',
      'Tom Ford': 'Tom Ford'
    }
  },
  {
    key: 'scentNotes',
    title: 'Scent Notes',
    valueMap: {
      'Amber': 'Amber',
      'Citrus': 'Citrus',
      'Floral': 'Floral',
      'Fresh': 'Fresh',
      'Fruity': 'Fruity',
      'Oriental': 'Oriental',
      'Rum': 'Rum',
      'Spice': 'Spice',
      'Woody': 'Woody'
    }
  },
  {
    key: 'price',
    title: 'Price',
    valueMap: {
      '15:50': 'AU $15 - 50',
      '50:200': 'AU $50 - 200',
      '200:500': 'AU $200 - 500'
    }
  }
];

const Home = () => {
  const [query, setQuery] = useState({});
  const [products, setProducts] = useState([]);

  const location = useLocation();

  useEffect(() => {
    if (Object.entries(query).length) {
      // Empty query search
      setQuery({});
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [location]);

  useEffect(() => {
    queryItems(query).then((items) => {
      console.log('items', items);
      setProducts(items);
    }).catch((error) => {
      console.error(error);
      message.error((error && error.message) || "Unknown error");
    });
  }, [query]);

  return (
    <Fragment>
      {/* side cortegray */}
      <Sider
        width={200}
        className="site-layout-background"
        style={{
          overflowY: "auto",
          height: "100%",
          position: "fixed",
          left: 0,
        }}
      >
        <Menu
          mode="inline"
          defaultOpenKeys={CATEGORY.map((item) => `sub-${item.key}`)}
          style={{ borderRight: 0 }}
        >
          {CATEGORY.map((categoryItem) => (
            <SubMenu key={`sub-${categoryItem.key}`} title={categoryItem.title} style={{ fontSize: "16px" }}>
              {Object.entries(categoryItem.valueMap).map(([value, label]) => (
                <Menu.Item key={value} onClick={() => setQuery({
                  [categoryItem.key]: value
                })}>{label}</Menu.Item>
              ))}
            </SubMenu>
          ))}
        </Menu>
      </Sider>

      {/* content */}
      <Layout style={{ marginLeft: 200 }}>
        {/* tag */}
        <Breadcrumb style={{ margin: "30px 25px 10px" }}>
          <Breadcrumb.Item>Home</Breadcrumb.Item>
          <Breadcrumb.Item>Products</Breadcrumb.Item>
        </Breadcrumb>

        {/* product */}
        <Content
          style={{
            padding: 24,
            height: "100%",
            minHeight: "90vh",
            overflowY: "auto",
          }}
        >
          <Space size="large" wrap>
          
            {products.map((itemData) => <Item itemData={itemData} key={'HomeItemList-' + itemData.id}></Item>)}
          </Space>
        </Content>
      </Layout>
    </Fragment>
  );
};

export default Home;
