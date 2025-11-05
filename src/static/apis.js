const API = "";
const crudAPI = `${API}/crud`;

async function getItems(table) {
  const response = await fetch(`${crudAPI}/${table}`);
  const data = await response.json();
  console.log(`Fetched data from ${table}:`, data);
  return data;
}

async function createItem(table, data) {
  const response = await fetch(`${crudAPI}/${table}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  const result = await response.json();
  console.log(`Created item in ${table}:`, result);
  return result;
}

async function updateItem(table, item_id, data) {
  const response = await fetch(`${crudAPI}/${table}/${item_id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  const result = await response.json();
  console.log(`Updated item in ${table}:`, result);
  return result;
}

async function deleteItem(table, item_id) {
  const response = await fetch(`${crudAPI}/${table}/${item_id}`, {
    method: "DELETE",
  });
  const result = await response.json();
  console.log(`Deleted item from ${table}:`, result);
  return result;
}

async function getInventory(sku, country) {
  const response = await fetch(
    `${API}/inventory?sku=${sku}&country=${country}`
  );
  const data = await response.json();
  console.log(`Inventory for ${sku} in ${country}:`, data);
  return data;
}
