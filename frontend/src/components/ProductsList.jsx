import React, { useEffect, useState } from "react";
import axios from "axios";

export default function ProductsList({ onSelectProduct }) {
    const [products, setProducts] = useState([]);
    const API_URL = `${import.meta.env.VITE_API_URL}/products/`;

    useEffect(() => {
        axios.get(API_URL).then((res) => setProducts(res.data));
    }, []);

    return (
        <div style={{ padding: 20 }}>
            <h1>Products</h1>
            <div style={{ display: "flex", flexWrap: "wrap", gap: 20 }}>
                {products.map((p) => (
                    <div
                        key={p.id}
                        style={{
                            border: "1px solid #ccc",
                            borderRadius: 10,
                            padding: 10,
                            width: 200,
                            cursor: "pointer",
                            textAlign: "center",
                            boxShadow: "2px 2px 6px rgba(0,0,0,0.1)",
                        }}
                        onClick={() => onSelectProduct(p.id)}
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
