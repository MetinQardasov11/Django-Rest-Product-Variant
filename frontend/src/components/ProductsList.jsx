import React, { useEffect, useState } from "react";
import axios from "axios";

export default function ProductsList({ categoryId, onSelectProduct }) {
    const [products, setProducts] = useState([]);
    const [attributes, setAttributes] = useState({});
    const [selectedFilters, setSelectedFilters] = useState({});

    useEffect(() => {
        if (!categoryId) return;

        // 1️⃣ Category attribute-lərini fetch et
        axios
            .get(`${import.meta.env.VITE_API_URL}/category/${categoryId}/attributes/`)
            .then((res) => setAttributes(res.data.attributes));

        // 2️⃣ Category məhsullarını fetch et
        axios
            .get(`${import.meta.env.VITE_API_URL}/products/?category=${categoryId}`)
            .then((res) => setProducts(res.data));
    }, [categoryId]);

    const handleFilterChange = (attr, value) => {
        setSelectedFilters((prev) => ({ ...prev, [attr]: value }));
    };

    // Filter-lənmiş products
    const filteredProducts = products.filter((p) =>
        Object.entries(selectedFilters).every(([attr, val]) => {
            if (!val) return true;
            return p.variants.some((v) =>
                v.attributes.some((a) => a.attribute_name === attr && a.value === val)
            );
        })
    );

    return (
        <div style={{ padding: 20 }}>
            <h2>Products</h2>

            {/* Dynamic attribute filters */}
            {Object.entries(attributes).map(([attr, values]) => (
                <label key={attr} style={{ marginRight: 15 }}>
                    {attr}:
                    <select
                        value={selectedFilters[attr] || ""}
                        onChange={(e) => handleFilterChange(attr, e.target.value)}
                        style={{ marginLeft: 5, padding: 3 }}
                    >
                        <option value="">Seçin</option>
                        {values.map((v) => (
                            <option key={v} value={v}>
                                {v}
                            </option>
                        ))}
                    </select>
                </label>
            ))}

            {/* Products grid */}
            <div
                style={{
                    display: "flex",
                    flexWrap: "wrap",
                    gap: 20,
                    marginTop: 20,
                }}
            >
                {filteredProducts.map((p) => (
                    <div
                        key={p.id}
                        onClick={() => onSelectProduct(p.id)}
                        style={{
                            border: "1px solid #ccc",
                            borderRadius: 10,
                            padding: 10,
                            width: 200,
                            cursor: "pointer",
                            textAlign: "center",
                            boxShadow: "2px 2px 6px rgba(0,0,0,0.1)",
                        }}
                    >
                        <img
                            src={p.image ? p.image : "/placeholder.png"}
                            alt={p.name}
                            style={{ width: "100%", height: 150, objectFit: "cover" }}
                        />
                        <h3>{p.name}</h3>
                    </div>
                ))}
            </div>
        </div>
    );
}
