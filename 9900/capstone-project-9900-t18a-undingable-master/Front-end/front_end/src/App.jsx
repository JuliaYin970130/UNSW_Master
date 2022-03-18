import {
  HashRouter as Router,
  Switch
} from 'react-router-dom';
import DefaultLayout from './layouts/DefaultLayout';

// Page import
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Admin from './pages/Admin';
import User from './pages/User';
import Cart from './pages/Cart';
import Questionaire from './pages/Questionaire';
import ItemInfo from './pages/ItemInfo';
import Search from './pages/Search';
import Checkout from './pages/Checkout';
import AdminManage from './pages/AdminManage';
import Evaluation from './pages/Evaluation';
import ItemManage from './pages/ItemManage';

import './App.less';

function App() {
  return (
      <Router>
          {/* A <Switch> looks through its children <Route>s and
              renders the first one that matches the current URL. */}
          <Switch>
              <DefaultLayout path="/admin" component={Admin} />
              <DefaultLayout path="/adminManage" component={AdminManage} />
              <DefaultLayout path="/itemManage" component={ItemManage} />
              <DefaultLayout path="/user" component={User} />
              <DefaultLayout path="/login" component={Login} />
              <DefaultLayout path="/reg" component={Register} />
              <DefaultLayout path="/questionaire" component={Questionaire} />
              <DefaultLayout path="/itemInfo" component={ItemInfo} />
              <DefaultLayout path="/search" component={Search} />
              <DefaultLayout path="/cart" component={Cart} />
              <DefaultLayout path="/checkout" component={Checkout} />
              <DefaultLayout path="/eval" component={Evaluation} />
              <DefaultLayout path="/" component={Home} />
          </Switch>
      </Router>
  );
}

export default App;
