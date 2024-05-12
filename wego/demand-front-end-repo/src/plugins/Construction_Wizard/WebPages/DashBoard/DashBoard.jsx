import { useNavigate } from 'react-router-dom';
import './DashBoard.css'

function DashBoard({ NavigationComponent }){
    const navigate = useNavigate();

    return (
        <>
            <NavigationComponent /> {/* Directly render the NavigationComponent */}
            <div className="DashBoard-Body-Container">
                <div className="Body-Text-Content">
                    <h1>
                        Construction Wizard
                    </h1>
                    <button id='create-project-button'onClick={() => navigate('/products/Construction_Wizard/create_project')}>Start Project</button>
                </div>
                <div className="Body-Image-Container">
                    <img src="/CW-Dashboard.png" alt="Dashboard" />
                </div>
            </div>
        </>
    );
};

export default DashBoard;