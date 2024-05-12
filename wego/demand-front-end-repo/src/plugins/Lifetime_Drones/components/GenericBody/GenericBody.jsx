import { useNavigate } from 'react-router-dom';
import './GenericBody.css'
import { useEffect, useState } from 'react';
import React from 'react';
import { ENV } from '../../../../constants';

function GenericBody({ title, items, itemType, imageSrc }) {

    const navigate = useNavigate();

    const [itemCount, setItemCount] = useState(items.length);
    const [itemList, setItemList] = useState(items)

    useEffect(() => {
        // Update itemCount when items prop changes
        setItemCount(items.length);

    }, [items.length]); // Reacting only to changes in items.length

    // Determine the background color based on the number of items
    const changeSideBarFlexGrowthRate = () => {
        if (itemCount >= 2) {
            return { flexGrow: .60 };  // Two or more Items
        } else if (itemCount == 1) {
            return { flexGrow: .30 };  // One Item
        } else {
            return { flexGrow: .20 };  // Zero Items
        }
    }
    // Function to handle navigation based on item type
    const handleNavigation = (path) => () => navigate(path);

    // const handleSelectionNavigation = (url_param) => {
    //     console.log(url_param)
    //     //check if the url is a project name to trim whitespace from url
    //     if (typeof url_param === 'string') {
    //         const trimmedUrl_param = url_param.name.trim()
    //         navigate(`/products/Construction_Wizard/${trimmedUrl_param}/orders`)
    //     } else {
    //         navigate(`/products/Construction_Wizard/${url_param}/orders`)
    //     }
    // }

    async function deleteProject(itemToDelete) {
        const baseUrl = ENV.API_BASE_URL_9000
        const api = (`${baseUrl}/demand-services/construction-wizard/delete_project/`)
        const projectData = { projectName: itemToDelete.name }; // Sending project name as data

        try {
            const response = await axios.post(api, projectData);
            if (response.status === 200) {
                console.log("SUCCESSFULLY DELETED PROJECT");
                const newProjectList = itemList.filter((item) => item.name !== itemToDelete.name);
                setItemList(newProjectList);
            }
        } catch (error) {
            console.error("ERROR WHILE DELETING PROJECT: ", error);
            alert("AN ERROR OCCURRED WHILE DELETING THE PROJECT");
        }
    }

    async function deleteOrder(order) {
        const baseUrl = ENV.API_BASE_URL_9000
        const api = (`${baseUrl}/demand-services/lifetime-drones/cancel_order/`)
        const OrderData = { order_id: order.id }; // Sending Order_id to delete in the backend

        try {
            const response = await axios.post(api, OrderData);
            if (response.status === 200) {
                alert(`SUCCESSFULLY DELETED ORDER ${order.id}`);
                const newOrderList = itemList.filter(item => item.id !== order.id);
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
                        {items.length > 0 && (
                            items.slice(0, 2).map((item, index) => (
                                <div key={index} className={`${itemType}-Selection-Container`}>
                                    <input onClick={handleNavigation(itemType === 'Project' ? `/products/Construction_Wizard/${items.name}/orders` : `/products/Construction_Wizard/orders/${items.id}`)}
                                        type="image"
                                        src={imageSrc}
                                        id='Click_Project'
                                    />
                                    {itemType === 'Order' ?
                                        <h2>{"Order#00" + item.id}</h2>
                                        :
                                        <>
                                            <h2>{item.name}</h2>
                                            <h1>{item.details}</h1>
                                        </>
                                    }

                                </div>
                            ))
                        )}
                    </div>
                </div>
                {itemType === "Order" ?
                    <>
                        <div className='Item-Box'> {/*Orders Side Panel Here*/}
                            <button id="Item" onClick={handleNavigation('/products/Lifetime_Drones/createOrder')}>😄 Create New Order</button>
                            {items.length > 0 &&
                                <button id="Item" onClick={() => deleteOrder(items[0])}>
                                    😄 Delete {"Order#00" + items[0].id}
                                </button>
                            }
                            {items.length > 1 &&
                                <button id="Item" onClick={() => deleteOrder(items[1])}>
                                    😄 Delete {"Order#00" + items[1].id}
                                </button>
                            }
                        </div>
                    </>
                    :
                    <>
                        <div className='Item-Box'> {/*Projects Side Panel Here*/}
                            <button id="Item" onClick={handleNavigation('/products/Construction_Wizard/create_project')}>😄 Create New Project</button>
                            {items.length > 0 &&
                                <button id="Item" onClick={() => deleteProject(items[0])}>
                                    😄 Delete {items[0].name}
                                </button>
                            }
                            {items.length > 1 &&
                                <button id="Item" onClick={() => deleteProject(items[1])}>
                                    😄 Delete {items[1].name}
                                </button>
                            }

                        </div>
                    </>
                }
            </div >
        </>
    )
}

export default GenericBody;