from django.utils.safestring import mark_safe
from django.shortcuts import redirect

MENUS = {
    "Connections": mark_safe(f"""<li class="menu-item" id="menu-db">
    <a href="{redirect('db').url}" class="menu-link">
      <i class='menu-icon tf-icons bx bx-data'></i>
      <div data-i18n="Connections">Connections</div>
    </a>
  </li>"""),
    "Schemas": mark_safe(f"""<li class="menu-item" id="menu-schema">
      <a href="{redirect('schemas').url}" class="menu-link">
        <i class="menu-icon tf-icons bx bx-windows"></i>
        <div data-i18n="Schemas">Schemas</div>
      </a>
  </li>"""),
    "Models": mark_safe(f"""<li class="menu-item" id="menu-models">
      <a href="{redirect('home').url}" class="menu-link">
        <i class="menu-icon tf-icons bx bxs-layout"></i>
        <div data-i18n="Models">Models</div>
      </a>
  </li>"""),
    "Data Tables": mark_safe(f"""<li class="menu-item" id="menu-tables">
      <a href="#" class="menu-link">
        <i class="menu-icon tf-icons bx bx-table"></i>
        <div data-i18n="Data Tables">Data Tables</div>
      </a>
  </li>"""),
    "Dashboard": mark_safe(f"""<li class="menu-item" id="menu-dash">
      <a href="#" class="menu-link">
        <i class="menu-icon tf-icons bx bxs-dashboard"></i>
        <div data-i18n="Dashboard">Dashboard</div>
      </a>
  </li>"""),
    "Sql Views": mark_safe(f"""<li class="menu-item" id="menu-views">
      <a href="{redirect('views_page').url}" class="menu-link">
        <i class="menu-icon tf-icons bx bx-file"></i>
        <div data-i18n="SQL Views">SQL Views</div>
      </a>
  </li>"""),
    "Authentication": mark_safe(f"""<li class="menu-item" id="menu-api-auth">
      <a href="{redirect('auth_list').url}" class="menu-link">
        <i class="menu-icon tf-icons bx bxs-lock"></i>
        <div data-i18n="Authentication">Authentication</div>
      </a>
  </li>"""),
    "Custom API": mark_safe(f"""<li class="menu-item" id="menu-api-meta">
      <a href="{redirect('api_meta_list').url}" class="menu-link">
        <i class="menu-icon tf-icons bx bx-code-block"></i>
        <div data-i18n="Custom API">Custom API</div>
      </a>
  </li>"""),
    "Core API": mark_safe(f"""<li class="menu-item" id="menu-core-api">
    <a href="{redirect('api_core_list').url}" class="menu-link">
      <i class="menu-icon tf-icons bx bx-code-alt"></i>
      <div data-i18n="Core API">Core API</div>
    </a>
  </li>"""),
    "Flow": mark_safe(f"""<li class="menu-item" id="menu-flow">
    <a href="#" class="menu-link">
      <i class='menu-icon tf-icons bx bxs-vial'></i>
      <div data-i18n="Flow">Flow</div>
    </a>
  </li>"""),
    "CMS Page": mark_safe(f"""<li class="menu-item" id="menu-cms">
    <a href="{redirect('cms_page').url}" class="menu-link">
      <i class='menu-icon bx bxs-book-content'></i>
      <div data-i18n="CMS Page">CMS Page</div>
    </a>
  </li>"""),
    "Schedule Jobs": mark_safe("""<li class="menu-item">
    <a href="/etlstudio" class="menu-link">
      <i class='menu-icon bx bxs-timer'></i>
      <div data-i18n="Scheduled Jobs">Scheduled Jobs</div>
    </a>
  </li>""")
}
