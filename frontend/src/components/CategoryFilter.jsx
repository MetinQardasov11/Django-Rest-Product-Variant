import React, { useEffect, useState } from "react";
import axios from "axios";

export default function CategoryFilter({ onSelectCategory }) {
    const [categories, setCategories] = useState([]);
    const API_URL = `${import.meta.env.VITE_API_URL}/categories/`; // category list endpoint

    useEffect(() => {
        axios.get(API_URL).then((res) => setCategories(res.data));
    }, []);

    return (
        <div style={{ padding: 20 }}>
            <label style={{ fontWeight: "bold" }}>
                Category:
                <select
                    onChange={(e) => onSelectCategory(e.target.value)}
                    defaultValue=""
                    style={{ marginLeft: 10, padding: 5 }}
                >
                    <option value="">Seçin</option>
                    {categories.map((c) => (
                        <option key={c.id} value={c.id}>
                            {c.name}
                        </option>
                    ))}
                </select>
            </label>
        </div>
    );
}
