const grid = document.getElementById("grid");
const emptyState = document.getElementById("empty-state");
const itemCount = document.getElementById("item-count");
const categoryFilter = document.getElementById("filter-category");
const modalBackdrop = document.getElementById("modal-backdrop");
const modalTitle = document.getElementById("modal-title");
const form = document.getElementById("item-form");
const toast = document.getElementById("toast");

const fieldId = document.getElementById("item-id");
const fieldName = document.getElementById("field-name");
const fieldCategory = document.getElementById("field-category");
const fieldPrice = document.getElementById("field-price");
const fieldStock = document.getElementById("field-stock");
const fieldDescription = document.getElementById("field-description");
const fieldImage = document.getElementById("field-image");

let allItems = [];

function showToast(message) {
  toast.textContent = message;
  toast.hidden = false;
  setTimeout(() => { toast.hidden = true; }, 2500);
}

function money(value) {
  return value.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
}

async function loadItems() {
  const params = new URLSearchParams();
  if (categoryFilter.value) params.set("category", categoryFilter.value);

  const res = await fetch(`/items?${params.toString()}`);
  allItems = await res.json();
  renderCategoryOptions();
  renderGrid();
}

function renderCategoryOptions() {
  const current = categoryFilter.value;
  const categories = [...new Set(allItems.map((i) => i.category))].sort();
  categoryFilter.innerHTML = '<option value="">Todas as categorias</option>' +
    categories.map((c) => `<option value="${c}">${c}</option>`).join("");
  categoryFilter.value = current;
}

function renderGrid() {
  itemCount.textContent = `${allItems.length} ${allItems.length === 1 ? "item" : "itens"}`;
  emptyState.hidden = allItems.length !== 0;
  grid.innerHTML = allItems.map((item) => `
    <div class="card">
      <img src="${item.image_url}" alt="${item.name}" loading="lazy" />
      <div class="card-body">
        <span class="card-category">${item.category}</span>
        <div class="card-name">${item.name}</div>
        <div class="card-desc">${item.description || ""}</div>
        <div class="card-meta">
          <span class="card-price">${money(item.price)}</span>
          <span class="card-stock">${item.stock} em estoque</span>
        </div>
      </div>
      <div class="card-actions">
        <button class="edit" onclick="openEdit(${item.id})">Editar</button>
        <button class="delete" onclick="removeItem(${item.id})">Excluir</button>
      </div>
    </div>
  `).join("");
}

function openModal() { modalBackdrop.hidden = false; }
function closeModal() { modalBackdrop.hidden = true; form.reset(); fieldId.value = ""; }

function openCreate() {
  modalTitle.textContent = "Novo item";
  form.reset();
  fieldId.value = "";
  openModal();
}

window.openEdit = function (id) {
  const item = allItems.find((i) => i.id === id);
  if (!item) return;
  modalTitle.textContent = "Editar item";
  fieldId.value = item.id;
  fieldName.value = item.name;
  fieldCategory.value = item.category;
  fieldPrice.value = item.price;
  fieldStock.value = item.stock;
  fieldDescription.value = item.description || "";
  fieldImage.value = item.image_url || "";
  openModal();
};

window.removeItem = async function (id) {
  if (!confirm("Excluir este item do catálogo?")) return;
  await fetch(`/items/${id}`, { method: "DELETE" });
  showToast("Item excluído");
  loadItems();
};

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const payload = {
    name: fieldName.value,
    category: fieldCategory.value,
    price: parseFloat(fieldPrice.value),
    stock: parseInt(fieldStock.value, 10),
    description: fieldDescription.value || null,
    image_url: fieldImage.value || null,
  };

  const id = fieldId.value;
  const res = await fetch(id ? `/items/${id}` : "/items", {
    method: id ? "PUT" : "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    showToast("Erro ao salvar item");
    return;
  }

  showToast(id ? "Item atualizado" : "Item criado");
  closeModal();
  loadItems();
});

document.getElementById("btn-new").addEventListener("click", openCreate);
document.getElementById("btn-cancel").addEventListener("click", closeModal);
categoryFilter.addEventListener("change", loadItems);
modalBackdrop.addEventListener("click", (e) => {
  if (e.target === modalBackdrop) closeModal();
});

loadItems();
