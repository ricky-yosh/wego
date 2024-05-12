import './AddressInput.css'

function AddressInput({ label, address, setAddress }) {
    const handleChange = (event) => {
        const { name, value } = event.target;
        setAddress(prevAddress => ({ ...prevAddress, [name]: value }));
    };

    return (
        <div className="co-address-input">
            <label>{label}</label>
            <input name="street" value={address.street} onChange={handleChange} placeholder='Street' className="co-address-input-field" />
            <input name="city" value={address.city} onChange={handleChange} placeholder='City' className="co-address-input-field" />
            <input name="state" value={address.state} onChange={handleChange} placeholder='State' className="co-address-input-field" />
            <input name="zipcode" value={address.zipcode} onChange={handleChange} placeholder='Zipcode' className="co-address-input-field" />
            <input name="county" value={address.county} onChange={handleChange} placeholder='County' className="co-address-input-field" />
        </div>
    );
}

export default AddressInput;