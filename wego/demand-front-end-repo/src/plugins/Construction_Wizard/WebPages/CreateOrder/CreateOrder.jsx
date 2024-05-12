import { useState, useEffect, useContext } from 'react';
import axios from "axios";
import { ENV } from '../../../../constants';
import './CreateOrder.css'
import AuthContext from '/src/utilities/AuthContext.jsx';
import { useParams } from 'react-router-dom';

function CreateOrder({ NavigationComponent, AddressInputComponent }) {

    const { project_name } = useParams(); // Destructuring to get params

    // Access user from the AuthContext
    const { user } = useContext(AuthContext);

    const initialItemState = {
        "item_id": "",
        "name": "",
        "price": 0,
        "description": "",
        "quantity": 1
    };

    const initialPickupAddressState = {
        "street": "",
        "city": "",
        "state": "",
        "zipcode": "",
        "county": ""
    };

    const initialDropoffAddressState = {
        "street": "",
        "city": "",
        "state": "",
        "zipcode": "",
        "county": ""
    };

    const [items, setItems] = useState([])
    const [cart, setCart] = useState([]) //used to store items in the cart for submit order
    const [item, updateItem] = useState(initialItemState) //used to update info depending on the selection of the item
    const [pickupAddress, setPickupAddress] = useState(initialPickupAddressState);
    const [dropoffAddress, setDropoffAddress] = useState(initialDropoffAddressState);
    const [vehicleType, setVehicleType] = useState("Car")
    const [inventory, setInventory] = useState([]); // State to store inventory data

    useEffect(() => {
        get_Inventory(); // Load inventory when component mounts
    }, []);

    function resetStates() {
        setItems([])
        setCart([])
        updateItem(initialItemState)
        setPickupAddress(initialPickupAddressState)
        setDropoffAddress(initialDropoffAddressState)
        setVehicleType("Car")
    }
    function addItemToCart() {
        const itemNotSelected = item.item_id === "";
        const quanityNotGiven = item.quantity <= 0;
        if (itemNotSelected) { alert("PLEASE SELECT ITEMS BEFORE PUTTING THEM IN THE CART") }
        if (quanityNotGiven) { alert("PLEASE SELECT A QUANTITY AMOUNT") }
        if (itemNotSelected && quanityNotGiven) { alert("PLEASE SELECT A QUANTITY AMOUNT AND A ITEM TO ADD TO CART") }

        if (!itemNotSelected && !quanityNotGiven) {
            setCart(prevCart => ([
                ...prevCart,
                { "name": item.name, "quantity": item.quantity, "price": item.price }
            ]));
            setItems(prevItems => ([
                ...prevItems,
                { "item_id": item.item_id, "quantity": parseInt(item.quantity, 10) }
            ]));
            updateItem(prevItem => prevItem = item);
        }
    }

    async function get_Inventory() {
        const baseUrl = ENV.API_BASE_URL_9000;
        const api = `${baseUrl}/demand-services/construction-wizard/get-inventory/`;

        try {
            const response = await axios.get(api);
            if (response.status === 200) {
                console.log("Successfully retrieved inventory data");
                setInventory(response.data.inventory); // Set the inventory data from the response
            }
        } catch (error) {
            console.error("Error grabbing inventory details", error.response ? error.response.data : error);
        }
    }

    function handleInput(event) {
        const { name, value } = event.target;
        if (name === "quantity") {
            if (!item.name) {  // Check if an item is selected
                alert("Please select an item before entering a quantity.");
                updateItem(prevItem => ({
                    ...prevItem,
                    quantity: 1  // Reset quantity to default
                }));
                return;  // Exit the function to prevent updating the quantity
            }

            if (value === "-") {
                value = "";  // Prevent negative or non-numeric input
            }

            const currentPrice = getItemDetails(item.name).price;  // Get current price per unit from the selected item
            updateItem(prevItem => ({
                ...prevItem,
                quantity: value,
                price: (currentPrice * value).toFixed(2)  // Calculate new price based on the new quantity
            }));
        } else if (name === "name") {
            const itemDetails = getItemDetails(value);  // Get the details of the newly selected item
            updateItem({
                ...initialItemState,
                ...itemDetails,
                "quantity": 1,
                price: itemDetails.price  // Ensure the price is set based on the selected item's price
            });
        } else if (name === "vehicle_type") {
            setVehicleType(value);
        }
    }


    function getItemDetails(itemName) {
        const item = inventory.find(i => i.name === itemName);
        return item || initialItemState;
    }

    // This function will check if all the required data is present
    function canSubmit() {
        return cart.length > 0 && vehicleType &&
            pickupAddress.street && pickupAddress.city && pickupAddress.state &&
            dropoffAddress.street && dropoffAddress.city && dropoffAddress.state;
    }

    const submitOrder = async (event) => {
        event.preventDefault(); // Prevent the default form submission
        if (!canSubmit()) {
            alert("Please fill in all required fields.");
            return;
        }

        const orderData = {
            "username": user.username,
            "items": items,
            "pickup_address": pickupAddress,
            "dropoff_address": dropoffAddress,
            "vehicle_type": vehicleType
        };
        const baseUrl = ENV.API_BASE_URL_9000;
        const createOrderEndpoint = (`${baseUrl}/demand-services/construction-wizard/create-and-submit-order/`);
        const OrderToProjectEndpoint = (`${baseUrl}/demand-services/construction-wizard/add-order-to-project/`);

        const createOrderResponse = await axios.post(createOrderEndpoint, orderData);

        //order successfully requested
        if (createOrderResponse.status === 200) {

            const order_id = createOrderResponse.data['order_id'];

            const ProjectOrderData = {
                "project_name": project_name,
                "username": user.username,
                "order_id": order_id
            };

            const addToProjectResponse = await axios.post(OrderToProjectEndpoint, ProjectOrderData);

            if (addToProjectResponse.status === 200) {
                alert("SUCCESSFULLY CREATED AND ADDED ORDER TO PROJECT");
                resetStates();
            } else {
                alert("ERROR CREATING ORDER FOR PROJECT");
            }

        } else if (createOrderResponse.status === 201) {
            alert("ORDER CREATED SUCCESSFULLY");
        }
    }

    return (
        <>
            <NavigationComponent projectName={project_name} pageType={"CreateOrder"} />
            <div className="co-body-container">
                <div className="co-container">
                    <h1 className="co-form-header">Submit Order</h1>
                    <form onSubmit={submitOrder} className="co-form">
                        <div className="co-form-group">
                            <label htmlFor="itemSelect">Choose an Item:</label>
                            <select onChange={handleInput} name="name" className="co-select">
                                <option value="">Select an item</option>
                                {inventory.map(item => (
                                    <option key={item.item_id} value={item.name}>{item.name} - ${item.price}</option>
                                ))}
                            </select>
                        </div>
                        <div className="co-form-group">
                            <label>Quantity</label>
                            <input onChange={handleInput} value={item.quantity} name="quantity" className="co-input" placeholder='Quantity Number' />
                        </div>
                        <div className="co-form-group">
                            <button type="button" className="co-button" onClick={addItemToCart}>Add Item</button>
                        </div>
                        <AddressInputComponent label="From:" address={pickupAddress} setAddress={setPickupAddress} />
                        <AddressInputComponent label="To:" address={dropoffAddress} setAddress={setDropoffAddress} />
                        <div className="co-form-group">
                            <label>Choose a Type of Vehicle:</label>
                            <select onChange={handleInput} name="vehicle_type" className="co-select">
                                <option value="Car">Car</option>
                                <option value="Truck">Truck</option>
                            </select>
                        </div>
                        <button type="submit" className="co-button" disabled={!canSubmit()}>Submit Order</button>
                    </form>
                    <div className="co-cart">
                        <h2>Cart Items</h2>
                        {cart.length > 0 ? (
                            <ul>
                                {cart.map((item, index) => (
                                    <li key={index}>
                                        {item.quantity} x {item.name} - ${item.price}
                                    </li>
                                ))}
                            </ul>
                        ) : (
                            <p>No items in the cart.</p>
                        )}
                    </div>
                </div>
            </div>
        </>
    );
}
export default CreateOrder;