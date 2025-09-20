import React, { useEffect, useState } from "react";
import axios from "axios";

export default function ProductDetail({ productId, onBack }) {
    const [product, setProduct] = useState(null);
    const [selected, setSelected] = useState({});
    const [activeVariant, setActiveVariant] = useState(null);
    const [inWishlist, setInWishlist] = useState(false);
    const [message, setMessage] = useState("");

    const API_URL = `${import.meta.env.VITE_API_URL}/products/${productId}/`;


    useEffect(() => {
        // Məhsulu götür
        axios.get(API_URL).then((res) => {
            const p = res.data;
            setProduct(p);

            const defaultVariant =
                p.variants.find((v) => v.stock > 0) || p.variants[0] || null;
            setActiveVariant(defaultVariant);

            // Əgər default variant varsa, wishlist statusunu yoxla
            if (defaultVariant) checkWishlist(defaultVariant.id);
        });
    }, [productId]);

    // Variant seçimi dəyişəndə
    const updateVariant = (attrName, value) => {
        const newSel = { ...selected, [attrName]: value };
        setSelected(newSel);

        if (product) {
            const match = product.variants.find((v) =>
                v.attributes.every((a) => newSel[a.attribute_name] === a.value)
            );
            if (match) {
                setActiveVariant(match);
                checkWishlist(match.id);
            }
        }
    };

    // ✅ Wishlist statusunu yoxlayan funksiya
    const checkWishlist = (variantId) => {
        axios
            .get(`${import.meta.env.VITE_API_URL}/wishlist/`, {
                headers: { Authorization: `Token 2a0a9e0f8117a1bc4cfbd97ce60acd9490fb138c` },
            })
            .then((res) => {
                const exists = res.data.some((item) => item.variant === variantId);
                setInWishlist(exists);
            })
            .catch(() => setInWishlist(false));
    };

    const toggleWishlist = () => {
        if (!activeVariant) {
            setMessage("Variant seçilməyib!");
            return;
        }

        if (!inWishlist) {
            axios
                .post(
                    `${import.meta.env.VITE_API_URL}/wishlist/`,
                    { variant: activeVariant.id },
                    { headers: { Authorization: `Token 2a0a9e0f8117a1bc4cfbd97ce60acd9490fb138c` } }
                )
                .then(() => {
                    setInWishlist(true);
                    setMessage("Variant wishliste əlavə edildi!");
                })
                .catch(() => setMessage("Xəta baş verdi!"));
        } else {
            axios
                .delete(
                    `${import.meta.env.VITE_API_URL}/wishlist/${activeVariant.id}/`,
                    { headers: { Authorization: `Token 2a0a9e0f8117a1bc4cfbd97ce60acd9490fb138c` } }
                )
                .then(() => {
                    setInWishlist(false);
                    setMessage("Variant wishliste-dən çıxarıldı!");
                })
                .catch(() => setMessage("Xəta baş verdi!"));
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

                            {/* ⭐ Wishlist düyməsi */}
                            <button
                                onClick={toggleWishlist}
                                disabled={activeVariant.stock === 0}
                                style={{
                                    marginTop: 10,
                                    padding: "8px 16px",
                                    backgroundColor: inWishlist ? "#888" : "#ff4081",
                                    color: "white",
                                    border: "none",
                                    cursor: "pointer",
                                }}
                            >
                                {inWishlist ? "💔 Remove from Wishlist" : "❤️ Add to Wishlist"}
                            </button>

                            {message && <p style={{ marginTop: 10 }}>{message}</p>}
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
