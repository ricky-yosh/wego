import { useNavigate } from 'react-router-dom';
import './Navbar.css'

function Navbar() {
    const navigate = useNavigate();

    return (
        <div className="Navigation-Container">
            <div className="Button-Container">
                <button onClick={() => navigate('/')} >WeGo</button>
                <button onClick={() => navigate('/products/Lifetime_Drones/Home')} >Home</button>
                <button onClick={() => navigate('/products/Lifetime_Drones/createOrder')} >Create Order</button>
                <button>Order History</button>
            </div>
        </div>
    )
}

export default Navbar;