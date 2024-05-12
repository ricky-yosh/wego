import React from 'react';
import { BrowserRouter as Router, Route, Routes, useLocation, matchPath } from 'react-router-dom'
import Navigation from './components/Navbar/Navbar'; // Ensure this is the correct path to your Navbar component
import PrivateRoute from "./utilities/PrivateRoutes.jsx";
import { AuthProvider } from './utilities/AuthContext';

//Plugin Imports
//Construction Wizard
import DashBoard from './plugins/Construction_Wizard/WebPages/DashBoard/DashBoard.jsx'
import Create_project from './plugins/Construction_Wizard/WebPages/CreateProject/CreateProject.jsx'
import Navbar from './plugins/Construction_Wizard/components/Navbar/Navbar.jsx';
import GenericBody from './plugins/Construction_Wizard/components/GenericBody/GenericBody.jsx';
import Projects from './plugins/Construction_Wizard/WebPages/Projects/Projects.jsx';
import Orders from './plugins/Construction_Wizard/WebPages/Orders/Orders.jsx';
import CreateOrder from './plugins/Construction_Wizard/WebPages/CreateOrder/CreateOrder.jsx';
import AddressInput from './plugins/Construction_Wizard/WebPages/CreateOrder/components/AddressInput.jsx';
import OrderStatus from './plugins/Construction_Wizard/WebPages/OrderStatus/OrderStatus.jsx';
import OrderHistory from './plugins/Construction_Wizard/WebPages/OrderHistory/OrderHistory.jsx';

//Lifetime Drones
import LDDashBoard from './plugins/Lifetime_Drones/WebPages/DashBoard/DashBoard.jsx';
import LDNavbar from './plugins/Lifetime_Drones/components/Navbar/Navbar.jsx';
import LDCreateOrder from './plugins/Lifetime_Drones/WebPages/CreateOrder/CreateOrder.jsx';

// Routes
import Home from './components/Home/Home';
import Footer from './components/Footer/Footer';
import Login from './common-services/Login/Login';
import SignUp from './common-services/SignUp/SignUp';
import Products from './plugins/Products.jsx';

function App() {

  const ConditionalNav = () => {
    const location = useLocation();

    // Paths that should not display the Navbar
    const hideNavPaths = [
      '/products/Construction_Wizard/Home',
      '/products/Construction_Wizard/create_project',
      '/products/Construction_Wizard/projects',
      "/products/Construction_Wizard/:projectName/orderHistory",
      '/products/Construction_Wizard/:project_name/:order_id',
      "/products/Construction_Wizard/:project_name/createOrder",
      "/products/Construction_Wizard/:project_name/orders",
      "/products/Construction_Wizard/:project_name/order/:order_id",
      '/products/Lifetime_Drones/Home',
      '/products/Lifetime_Drones/createOrder'
    ];

    // Check if the current path should hide the Navbar
    const shouldHideNav = () => hideNavPaths.some(path => matchPath({ path, end: true }, location.pathname));

    return (
      !shouldHideNav() && <Navigation />
    );
  };

  return (
    <Router>
      <div>
        <AuthProvider>
          <ConditionalNav /> {/*This will not include the custom navbar for plugins*/}
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<SignUp />} />

            {/* Private Routes */}
            <Route path="/products" element={<PrivateRoute><Products /></PrivateRoute>} />
            <Route path="/products/Construction_Wizard/Home" element={<PrivateRoute><DashBoard NavigationComponent={Navbar} /></PrivateRoute>} />
            <Route path="/products/Construction_Wizard/:projectName/orderHistory" element={<PrivateRoute><OrderHistory NavigationComponent={Navbar} /></PrivateRoute>} />
            <Route path="/products/Construction_Wizard/create_project" element={<PrivateRoute><Create_project NavigationComponent={Navbar} /></PrivateRoute>} />
            <Route path="/products/Construction_Wizard/:project_name/createOrder" element={<PrivateRoute><CreateOrder NavigationComponent={Navbar} AddressInputComponent={AddressInput} /></PrivateRoute>} />
            <Route path="/products/Construction_Wizard/projects" element={<PrivateRoute><Projects NavigationComponent={Navbar} GenericBodyComponent={GenericBody} /></PrivateRoute>} />
            <Route path="/products/Construction_Wizard/:project_name/orders" element={<PrivateRoute><Orders NavigationComponent={Navbar} GenericBodyComponent={GenericBody} /></PrivateRoute>} />
            <Route path="/products/Construction_Wizard/:project_name/order/:order_id" element={<PrivateRoute><OrderStatus NavigationComponent={Navbar} /></PrivateRoute>} />
            <Route path="/products/Lifetime_Drones/Home" element={<PrivateRoute><LDDashBoard NavigationComponent={LDNavbar} /></PrivateRoute>} />
            <Route path="/products/Lifetime_Drones/createOrder" element={<PrivateRoute><LDCreateOrder NavigationComponent={LDNavbar} AddressInputComponent={AddressInput} /></PrivateRoute>} />
          </Routes>
        </AuthProvider>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
