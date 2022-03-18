import { Layout } from 'antd';
import {
    Route
} from 'react-router-dom';
import Header from '../../components/Header/Header';

import './index.css';

const DefaultLayout = ({component: Component, ...rest}) => {
    return (
        <Route {...rest} render={matchProps => (
            <Layout>
                <Header/>
                <Layout>
                    <Component {...matchProps} />
                </Layout>
            </Layout>
        )} />
    );
};

export default DefaultLayout;