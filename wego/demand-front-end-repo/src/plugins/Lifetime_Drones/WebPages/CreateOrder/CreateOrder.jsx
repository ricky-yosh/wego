import { useState, useEffect, useContext } from 'react';
import axios from "axios";
import { ENV } from '../../../../constants';
import './CreateOrder.css'
import AuthContext from '/src/utilities/AuthContext.jsx';
import { useParams } from 'react-router-dom';


function CreateOrder({ NavigationComponent, AddressInputComponent }) {

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

    const initial_vehicle_type = "Drone"

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
        updateItem(initialItemState)
        setPickupAddress(initialPickupAddressState)
        setDropoffAddress(initialDropoffAddressState)
        setVehicleType(initial_vehicle_type)
        setInventory([])

    }

    function addItemToCart() {
        setCart(prevCart => ([
            ...prevCart,
            { "name": item.name, "quantity": item.quantity, "price": item.price }
        ]));
        setItems(prevItems => ([
            ...prevItems,
            { "item_id": item.item_id, "quantity": parseInt(item.quantity, 10) }
        ]));
        updateItem(initialItemState);  // Reset 'item' to its initial state after adding to cart.
    }

    async function get_Inventory() {
        const baseUrl = ENV.API_BASE_URL_9000;
        const api = `${baseUrl}/demand-services/lifetime-drones/get-inventory/`;

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
    

    function getItemDetails(itemName) {
        const item = inventory.find(i => i.name === itemName);
        return item || initialItemState;
    }


    function handleInput(event) {
        const { name, value } = event.target;
        console.log(name)
        console.log(value)
        if (name === "quantity") {
            console.log(item.name)
            const currentPrice = getItemDetails(item.name).price; // Get current price per unit from the selected item
            updateItem(prevItem => ({
                ...prevItem,
                quantity: value,
                price: (currentPrice * value).toFixed(2) // Calculate new price based on the new quantity
            }));

        } else if (name === "name") {
            const itemDetails = getItemDetails(value); // Get the details of the newly selected item
            updateItem({
                ...initialItemState,
                ...itemDetails,
                "quantity": 1,
                price: itemDetails.price // Ensure the price is set based on the selected item's price
            });
        } else if (name === "vehicle_type") {
            setVehicleType(value);
        }
    }

    // This function will check if all the required data is present
    function canSubmit() {
        //return item.item_name && item.quantity > 0 &&
           // pickupAddress.street && pickupAddress.city && pickupAddress.state &&
           // dropoffAddress.street && dropoffAddress.city && dropoffAddress.state;
        if (cart.length > 0 &&
             pickupAddress.street && pickupAddress.city && pickupAddress.state && pickupAddress.county && pickupAddress.zipcode &&
             dropoffAddress.street && dropoffAddress.city && dropoffAddress.state && dropoffAddress.county && dropoffAddress.zipcode) {
                return true;
             }
        else {
            return false;
        }

    }
    const [isFormValid, setIsFormValid] = useState(false);
    
    useEffect(() => {
        // Update the isFormValid state whenever there's a change in the form inputs
        
        setIsFormValid(canSubmit());
        //console.log(isFormValid);
        //console.log(cart);
        //console.log(pickupAddress);
        //console.log(dropoffAddress);
    }, [item, pickupAddress, dropoffAddress]);

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
        console.log(orderData);
        const baseUrl = ENV.API_BASE_URL_9000;
        const createOrderEndpoint = (`${baseUrl}/demand-services/lifetime-drones/create-and-submit-order/`);
        const createOrderResponse = await axios.post(createOrderEndpoint, orderData);

        
        if (createOrderResponse.status === 200 || createOrderResponse.status == 201) {
            alert("Successfully created order");
            resetStates();
        } else {
            alert("Error Creating Order");
        }

    }

    return (
        <>
            <NavigationComponent />
            <div className="bg-container">
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
                            <input onChange={handleInput} value={item.quantity} name="quantity" className="co-input" placeholder='Quantity Number' required />
                        </div>
                        <div className="co-form-group">
                            <button type="button" className="co-button" onClick={addItemToCart}>Add Item</button>
                        </div>
                        <AddressInputComponent label="From:" address={pickupAddress} setAddress={setPickupAddress} />
                        <AddressInputComponent label="To:" address={dropoffAddress} setAddress={setDropoffAddress} />
                        <button type="submit" className="co-button" disabled={!isFormValid}>Submit Order</button>
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