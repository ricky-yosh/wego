import { useNavigate } from 'react-router-dom';
import './GenericBody.css'
import { useEffect, useState, useContext } from 'react';
import React from 'react';
import { ENV } from '../../../../constants';
import axios from 'axios';
import AuthContext from '/src/utilities/AuthContext.jsx';

function GenericBody({ title, items, itemType, imageSrc, urlParam }) {

    const { user } = useContext(AuthContext);

    const navigate = useNavigate();
    const [itemList, setItemList] = useState(items)

    useEffect(() => {
        setItemList(items);
    }, [items, user]); // Notice dependency on items and user


    // Determine the background flex grow of side panel based on the number of items
    const changeSideBarFlexGrowthRate = () => {
        if (itemList.length >= 2) {
            return { flexGrow: .60 };  // Two or more Items
        } else if (itemList.length == 1) {
            return { flexGrow: .30 };  // One Item
        } else {
            return { flexGrow: .20 };  // Zero Items
        }
    }

    // Function to handle navigation based on item type
    const handleNavigation = (path) => () => navigate(path);

    async function deleteProject(ProjectName) {
        const baseUrl = ENV.API_BASE_URL_9000
        const api = (`${baseUrl}/demand-services/construction-wizard/delete_project/`)
        const projectData = { "username": user.username, "project_name": ProjectName }; // Sending project name as data
        try {
            const response = await axios.post(api, projectData);
            if (response.status === 200) {
                const newProjectList = itemList.filter((item) => item.name !== ProjectName);
                setItemList(newProjectList)
                alert("SUCCESSFULLY DELETED PROJECT");
            }
        } catch (error) {
            alert("AN ERROR OCCURRED WHILE DELETING THE PROJECT");
        }
    }

    async function deleteProjectOrder(order_id) {
        const baseUrl = ENV.API_BASE_URL_9000
        const api = (`${baseUrl}/demand-services/construction-wizard/cancel-order/`)
        const OrderData = { "order_id": order_id }; // Sending Order_id to delete in the backend

        try {
            const response = await axios.post(api, OrderData);
            if (response.status === 200) {
                alert(`SUCCESSFULLY DELETED ORDER ${order_id}`);
                const newOrderList = itemList.filter(item => item.order_id !== order_id);
                setItemList(newOrderList);
            }
        } catch (error) {
            console.error("ERROR WHILE DELETING ORDER: ", error);
            alert("AN ERROR OCCURRED WHILE DELETING THE ORDER");
        }
    }


    return (
        <>
            <div className={`${itemType}-Template-Container`}>
                <div className={`${itemType}-Side-Bar-Container`} style={changeSideBarFlexGrowthRate()}></div>
                <div className={`${itemType}-Flex-Container`}>
                    <div className={`${itemType}-Content-Flex-Container`}>
                        <div className={`${itemType}-Description-Container`}>
                            <h1>{title}</h1>
                        </div>
                        {itemList.length > 0 && (
                            itemList.slice(0, 2).map((item, index) => (
                                <div key={index} className={`${itemType}-Selection-Container`}>
                                    <input
                                        onClick={handleNavigation(itemType === 'Project' ? `/products/Construction_Wizard/${item.name}/orders` : `/products/Construction_Wizard/${urlParam}/order/${item.order_id}`)}
                                        type="image"
                                        src={imageSrc}
                                        id='Click_Project'
                                    />
                                    {itemType === 'Order' ?
                                        <h2>{`Order#${index === 0 ? '001' : '002'}`}</h2> // Hardcode "001" for the first item and "002" for the second
                                        :
                                        <>
                                            <h2>{item.name}</h2>
                                            <h1>{item.orders} Orders pending</h1>
                                        </>
                                    }
                                </div>
                            ))
                        )}
                    </div>
                </div>
                {itemType === "Order" ?
                    <>
                        <div className='Item-Box'>
                            <button id="Item" onClick={handleNavigation(`/products/Construction_Wizard/${urlParam}/createOrder`)}>😄 Create New Order</button>
                            {itemList.length > 0 &&
                                <button id="Item" onClick={() => deleteProjectOrder(itemList[0].order_id)}>
                                    😄 Delete "Order#001"
                                </button>
                            }
                            {itemList.length > 1 &&
                                <button id="Item" onClick={() => deleteProjectOrder(itemList[1].order_id)}>
                                    😄 Delete "Order#002"
                                </button>
                            }
                        </div>
                    </>
                    :
                    <>
                        <div className='Item-Box'>
                            <button id="Item" onClick={handleNavigation('/products/Construction_Wizard/create_project')}>😄 Create New Project</button>
                            {itemList.length > 0 &&
                                <button id="Item" onClick={() => deleteProject(itemList[0].name)}>
                                    😄 Delete {itemList[0].name}
                                </button>
                            }
                            {itemList.length > 1 &&
                                <button id="Item" onClick={() => deleteProject(itemList[1].name)}>
                                    😄 Delete {itemList[1].name}
                                </button>
                            }
                        </div>
                    </>
                }
            </div>
        </>
    );


}

export default GenericBody;