/**
 * 大秦无人机低空周报 - 主题切换
 * 暗色/亮色双版面，偏好保存到 localStorage
 */
(function() {
  'use strict';

  var TOGGLE_ID = 'theme-toggle';
  var STORAGE_KEY = 'daqin-weekly-theme';

  // 读取已保存的主题偏好
  function getSavedTheme() {
    try {
      return localStorage.getItem(STORAGE_KEY);
    } catch (e) {
      return null;
    }
  }

  // 保存主题偏好
  function saveTheme(theme) {
    try {
      localStorage.setItem(STORAGE_KEY, theme);
    } catch (e) {}
  }

  // 应用主题
  function applyTheme(theme) {
    if (theme === 'dark') {
      document.documentElement.setAttribute('data-theme', 'dark');
    } else {
      document.documentElement.removeAttribute('data-theme');
    }
  }

  // 初始化
  function init() {
    var saved = getSavedTheme() || 'light';
    applyTheme(saved);

    // 创建切换按钮
    var isDark = saved === 'dark';
    var btn = document.createElement('button');
    btn.id = TOGGLE_ID;
    btn.className = 'theme-toggle';
    btn.title = isDark ? '切换到亮色版' : '切换到暗色版';
    btn.textContent = isDark ? '☀️' : '🌙';
    btn.setAttribute('aria-label', '切换主题');

    btn.addEventListener('click', function() {
      var current = document.documentElement.getAttribute('data-theme');
      var isDarkNow = (current === 'dark');
      var next = isDarkNow ? 'light' : 'dark';
      applyTheme(next);
      saveTheme(next);
      btn.textContent = (next === 'dark') ? '☀️' : '🌙';
      btn.title = (next === 'dark') ? '切换到亮色版' : '切换到暗色版';
    });

    document.body.appendChild(btn);
  }

  // DOM 加载完成后初始化
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
