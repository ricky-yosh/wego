import { useNavigate } from 'react-router-dom';
import './Navbar.css';

function Navbar({ projectName, pageType }) {
    const navigate = useNavigate();
    // Helper function to render buttons based on the page type
    function renderButtons(pageType) {
        let specificButton;
        if (pageType === "CreateOrder" || pageType === "OrderStatus") {
            specificButton = <button onClick={() => navigate(`/products/Construction_Wizard/${projectName}/orders`)}>Orders</button>;
        } else {
            specificButton = <button onClick={() => navigate('/products/Construction_Wizard/projects')}>Projects</button>;
        }

        return (
            <>
                <button onClick={() => navigate('/products')}>Wego</button>
                <button onClick={() => navigate('/products/Construction_Wizard/Home')}>Home</button>
                {pageType === "Orders" && (
                    <button onClick={() => navigate(`/products/Construction_Wizard/${projectName}/orderHistory`)}>Order History</button>
                )}
                {specificButton}
            </>
        );

    }

    return (
        <div className="Navigation-Container">
            {projectName && pageType !== "CreateOrder" && pageType !== "OrderStatus" && (
                <div className='Project-Name-Container'>
                    {`${projectName} Project Orders`}
                </div>
            )}
            <div className="Button-Container">
                {renderButtons(pageType)}
            </div>
        </div>
    );
}

export default Navbar;
