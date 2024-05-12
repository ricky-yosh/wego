import { useNavigate } from 'react-router-dom';
import './DashBoard.css'


function DashBoard({ NavigationComponent }){
    const navigate = useNavigate();

    return (
        <>
            <NavigationComponent /> {/* Directly render the NavigationComponent */}
            <div className="Background-Container">
                <div className="DashBoard-Body-Container">
                    <div className="Body-Text-Content">
                        <h1>
                            Lifetime Drones
                        </h1>
                        <button id='create-project-button'onClick={() => navigate('/products/Lifetime_Drones/createOrder')}>Create Order</button>
                    </div>
                    <div className="Body-Image-Container">
                        <img src="/LD-Dashboard.png" alt="Dashboard" />
                    </div>
                </div>
            </div>
        </>
    );
};

export default DashBoard;