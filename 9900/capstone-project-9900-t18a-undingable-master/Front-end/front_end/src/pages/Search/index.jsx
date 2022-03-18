import React from 'react';
import { useLocation } from 'react-router-dom';
import { Layout, Breadcrumb } from 'antd';
import qs from 'querystring';
import SearchList from '../../components/SearchList';

const { Content } = Layout;

const Search = () => {
    const location = useLocation();
    const parsedQuery = qs.parse(location.search.replace('?', ''));

    console.log('location', location);
    console.log('parsedQuery', parsedQuery);

    return (
        <Content style={{ marginTop: "64px", padding: '0 50px', minHeight: "720px" }}>
            {/* tag location */}
            <Breadcrumb style={{ margin: '16px 0' }}>
                <Breadcrumb.Item>Home</Breadcrumb.Item>
                <Breadcrumb.Item>Search</Breadcrumb.Item>
            </Breadcrumb>
            {/* search result */}
            <SearchList keyword={parsedQuery.keyword} />
        </Content>

    );
};

export default Search;
