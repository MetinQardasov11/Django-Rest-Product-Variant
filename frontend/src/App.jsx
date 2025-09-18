import React, { useState } from "react";
import CategoryFilter from "./components/CategoryFilter";
import ProductsList from "./components/ProductsList";
import ProductDetail from "./components/ProductDetail";

function App() {
    const [selectedProductId, setSelectedProductId] = useState(null);
    const [selectedCategory, setSelectedCategory] = useState(null);

    return (
        <div style={{ fontFamily: "Arial, sans-serif" }}>
            {!selectedProductId ? (
                <>
                    <CategoryFilter onSelectCategory={setSelectedCategory} />
                    <ProductsList
                        categoryId={selectedCategory}
                        onSelectProduct={setSelectedProductId}
                    />
                </>
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
