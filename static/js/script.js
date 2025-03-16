document.addEventListener("DOMContentLoaded", function () {
  // 获取表单和加载指示器
  const form = document.getElementById("upload-form");
  const convertBtn = document.getElementById("convert-btn");
  const spinner = document.getElementById("loading-spinner");
  const fileInput = document.getElementById("file");
  const formatSelect = document.getElementById("format");

  // 邮箱相关元素
  const emailSwitch = document.getElementById("send_email_enabled");
  const emailInputGroup = document.getElementById("email_input_group");
  const emailInput = document.getElementById("send_to_email");

  // 切换邮箱输入框的显示/隐藏
  emailSwitch.addEventListener("change", function () {
    if (this.checked) {
      emailInputGroup.classList.remove("d-none");
      emailInput.setAttribute("required", "required");
    } else {
      emailInputGroup.classList.add("d-none");
      emailInput.removeAttribute("required");
    }
  });

  // 提交表单时显示加载状态
  form.addEventListener("submit", function (e) {
    // 验证文件已选择
    if (fileInput.files.length === 0) {
      e.preventDefault();
      alert("请选择一个文件");
      return;
    }

    // 验证输出格式已选择
    if (formatSelect.value === "") {
      e.preventDefault();
      alert("请选择输出格式");
      return;
    }

    // 验证邮箱格式（如果启用了邮件发送）
    if (emailSwitch.checked && emailInput.value.trim() !== "") {
      const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
      if (!emailPattern.test(emailInput.value.trim())) {
        e.preventDefault();
        alert("请输入有效的邮箱地址");
        return;
      }
    }

    // 显示加载状态
    convertBtn.disabled = true;
    convertBtn.innerHTML =
      '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>正在转换...';
  });

  // 文件选择变化时显示文件名
  fileInput.addEventListener("change", function () {
    const fileName = this.files?.name;
    if (fileName) {
      const fileExtension = fileName.split(".").pop().toLowerCase();
      // 根据文件扩展名预选输出格式
      if (formatSelect.querySelector(`option[value="${fileExtension}"]`)) {
        // 不自动选择相同格式，让用户选择
        const options = Array.from(formatSelect.options);
        const currentFormat = options.findIndex(
          (opt) => opt.value === fileExtension
        );
        if (currentFormat > 0) {
          const nextFormat = (currentFormat + 1) % options.length;
          if (nextFormat > 0) {
            // 跳过第一个禁用的选项
            formatSelect.selectedIndex = nextFormat;
          } else {
            formatSelect.selectedIndex = 1;
          }
        }
      }
    }
  });
});
