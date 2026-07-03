export function calculateOrderTotal(items) {
    const total = items.reduce((sum, item) => {
        return sum + item.price * item.quantity;
    }, 0);

    console.log("Calculated order total:", total);

    return total;
}

export function applyDiscount(total, discountRate) {
    const discountAmount = total * discountRate;
    const finalTotal = total - discountAmount;

    console.log("Final total after discount:", finalTotal);

    return finalTotal;
}