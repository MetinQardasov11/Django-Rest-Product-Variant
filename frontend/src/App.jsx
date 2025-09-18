import React, { useState } from "react";
import ProductsList from "./components/ProductsList";
import ProductDetail from "./components/ProductDetail";

function App() {
    const [selectedProductId, setSelectedProductId] = useState(null);

    return (
        <div>
            {!selectedProductId ? (
                <ProductsList onSelectProduct={setSelectedProductId} />
            ) : (
                <ProductDetail
                    productId={selectedProductId}
                    onBack={() => setSelectedProductId(null)}
                />
            )}
        </div>
    );
}

export default App;
