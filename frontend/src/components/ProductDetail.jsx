import React, { useEffect, useState } from "react";
import axios from "axios";

export default function ProductDetail({ productId, onBack }) {
    const [product, setProduct] = useState(null);
    const [selected, setSelected] = useState({});
    const [activeVariant, setActiveVariant] = useState(null);

    const API_URL = `${import.meta.env.VITE_API_URL}/products/${productId}/`;

    useEffect(() => {
        axios.get(API_URL).then((res) => {
            const p = res.data;
            setProduct(p);

            const defaultVariant =
                p.variants.find((v) => v.stock > 0) || p.variants[0] || null;
            setActiveVariant(defaultVariant);
        });
    }, [productId]);

    const updateVariant = (attrName, value) => {
        const newSel = { ...selected, [attrName]: value };
        setSelected(newSel);

        if (product) {
            const match = product.variants.find((v) =>
                v.attributes.every((a) => newSel[a.attribute_name] === a.value)
            );
            if (match) setActiveVariant(match);
        }
    };

    if (!product) return <p>Loading…</p>;

    const grouped = {};
    product.variants.forEach((v) => {
        v.attributes.forEach((a) => {
            grouped[a.attribute_name] = grouped[a.attribute_name] || new Set();
            grouped[a.attribute_name].add(a.value);
        });
    });

    return (
        <div style={{ padding: 20 }}>
            <button onClick={onBack} style={{ marginBottom: 20 }}>
                ← Back
            </button>

            <div style={{ display: "flex", gap: 40 }}>
                <div>
                    <img
                        src={product.image ? product.image : "/placeholder.png"}
                        alt={product.name}
                        style={{ width: 300, height: 300, objectFit: "cover" }}
                    />
                </div>

                <div>
                    <h2>{product.name}</h2>
                    <p>{product.description}</p>

                    {Object.entries(grouped).map(([attr, values]) => (
                        <label key={attr} style={{ display: "block", marginBottom: 10 }}>
                            {attr}:
                            <select
                                value={selected[attr] || ""}
                                onChange={(e) => updateVariant(attr, e.target.value)}
                            >
                                <option value="">Seçin</option>
                                {[...values]
                                    .sort((a, b) => parseInt(a) - parseInt(b))
                                    .map((v) => (
                                        <option key={v} value={v}>
                                            {v}
                                        </option>
                                    ))}
                            </select>
                        </label>
                    ))}

                    {activeVariant && (
                        <>
                            <p>
                                Qiymət:{" "}
                                <span
                                    style={{
                                        color: activeVariant.stock > 0 ? "green" : "red",
                                        fontWeight: activeVariant.stock > 0 ? "normal" : "bold",
                                        animation:
                                            activeVariant.stock > 0 ? "none" : "flash 1s infinite",
                                    }}
                                >
                                    {activeVariant.stock > 0
                                        ? activeVariant.price + " ₼"
                                        : "Stokda bitib"}
                                </span>
                            </p>
                            <p>SKU: {activeVariant.sku}</p>
                        </>
                    )}
                </div>
            </div>

            <style>
                {`
          @keyframes flash {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
          }
        `}
            </style>
        </div>
    );
}
