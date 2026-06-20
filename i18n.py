LANGS = ("en", "ru")

STR = {
    "en": {
        "welcome_title": "◈  <b>Welcome to RetainX Studio</b>",
        "welcome_body": (
            "  The fastest and most affordable way\n"
            "  to generate AI video, images & audio.\n\n"
            "  ◉  Kling 3.0  ·  Veo 3.1  ·  Sora 2\n"
            "  ◉  Midjourney  ·  Flux  ·  Seedance\n"
            "  ◉  HeyGen  ·  ElevenLabs  ·  LTX\n\n"
            "  Up to <b>3× cheaper</b> than any competitor.\n"
            "  Results delivered in <b>~2 minutes.</b>"
        ),
        "welcome_bonus": "  🎁  <b>{bonus} free coins</b> added to your account.\n  Balance   <b>{coins} coins</b>",
        "what_create": "What would you like to create?",
        "choose_option": "Choose an option:",

        "main_menu_title": "◈  <b>RetainX Studio</b>",
        "main_menu_balance": "  Balance   <b>{coins} coins</b>",
        "main_menu_desc": "  Generate AI video, images & audio\n  at the most competitive rates.",

        "btn_video_generation": "▸  Video Generation",
        "btn_image_generation": "▸  Image Generation",
        "btn_audio_voice": "▸  Audio & Voice",
        "btn_wallet_coins": "◈  Wallet  ·  {coins} coins",
        "btn_pricing": "◎  Pricing",
        "btn_support": "◌  Support",
        "btn_language": "◐  Language",
        "btn_start_generating": "▸  Start Generating",
        "btn_view_pricing": "◎  View Pricing",
        "btn_back": "←  Back",

        "audio_title": "◌  <b>Audio & Voice</b>",
        "audio_body": "  Coming soon.\n\n  We are integrating voice synthesis\n  and music generation tools.\n\n  Stay tuned.",

        "support_title": "◌  <b>Support</b>",
        "support_body": "  Contact us: @RetainXStudio",

        "video_title": "◈  <b>Video Generation</b>",
        "select_category": "Select a category:",

        "images_title": "◈  <b>Image Generation</b>",
        "select_model": "Select a model:",

        "pricing_title": "◎  <b>Pricing</b>",
        "pricing_body": "  1 coin  =  <b>$0.05</b>\n\n  Select a category to view rates:",
        "btn_image_pricing": "▸  Image Pricing",
        "btn_video_pricing": "▸  Video Pricing",

        "menu_main_menu": "⌂  Main Menu",
        "menu_wallet": "◈  Wallet",
        "menu_video": "▸  Video",
        "menu_images": "▸  Images",
        "menu_audio": "▸  Audio",
        "menu_orders": "≡  Orders",
        "menu_support": "◌  Support",

        "lang_title": "◐  <b>Language</b>",
        "lang_desc": "  Choose your preferred language:",
        "lang_changed": "✓  Language updated.",

        "coins_word": "coins",

        # ── Image generation flow ──────────────────────────────
        "img_menu_title": "◈  <b>Image Generation</b>",
        "img_menu_select": "Select a model to continue:",
        "img_price_label": "Price",
        "img_per_gen": "per generation",
        "img_select_ar": "Select aspect ratio:",
        "img_select_quality": "Select quality:",
        "img_aspect_ratio_label": "Aspect ratio",
        "img_quality_label": "Quality",
        "img_cost_label": "Cost",
        "img_balance_label": "Your balance",
        "img_attach_optional": "  Attach reference images (optional)\n  or skip to write your prompt.",
        "img_btn_add_ref": "◈  Add Image Reference  (up to {max})",
        "img_btn_skip_prompt": "▸  Skip — Write Prompt",
        "img_enter_prompt": "Enter your prompt:",
        "img_order_summary_title": "◈  <b>Order Summary</b>",
        "img_model_label": "Model",
        "img_prompt_label": "Prompt:",
        "img_btn_confirm": "◈  Confirm  ({coins} coins)",
        "img_btn_edit_prompt": "✎  Edit Prompt",
        "img_edit_prompt_prompt": "✎  Enter your new prompt:",
        "img_session_expired": "Session expired. Please start your order again.",
        "img_insufficient_coins": "Insufficient coins. Please top up your wallet.",
        "img_order_placed_title": "◌  <b>Order #{oid} Placed</b>",
        "img_model_row": "  Model     <b>{name}</b>",
        "img_coins_deducted": "  Coins      <b>{coins} deducted</b>",
        "img_estimated_time": "  Estimated time  ~2 minutes",
        "img_will_deliver": "  We will deliver your image here shortly.",
        "img_ref_title": "◈  <b>Image Reference</b>  ({count}/{max})",
        "img_ref_instructions": (
            "  Send up to <b>{max} images</b> as reference.\n\n"
            "  <code>@img1</code>, <code>@img2</code> etc. are just labels\n"
            "  for you — the AI doesn't read them. Describe each image\n"
            "  in words in your prompt instead.\n\n"
            "  Tap <b>Done</b> when finished."
        ),
        "btn_done": "✓  Done",
        "img_ref_saved": "✓  Image @img{n} saved.  ({count}/{max})",
        "img_ref_send_more": "Send more or tap Done.",
        "img_ref_max_reached": "Maximum reached. Tap Done.",
        "img_ref_max_alert": "Maximum {max} images reached. Tap Done to continue.",
        "img_refs_attached": "  ◈  {count} image ref(s) attached\n",

        # ── Video generation flow ──────────────────────────────
        "vid_menu_title": "◈  <b>Video Generation</b>",
        "vid_select_category": "Select a category:",
        "vid_sub_standard": "▸  Standard Video",
        "vid_sub_premium": "▸  Premium Video",
        "vid_sub_kling": "▸  Kling Video",
        "vid_sub_avatar": "▸  Avatar & Dubbing",
        "vid_select_model": "Select a model:",
        "vid_unknown_tool": "Tool not found",
        "vid_resolution_word": "Resolution",
        "vid_duration_word": "Duration",
        "vid_sec_word": "sec",
        "vid_type_word": "Type",
        "vid_avatar_video_word": "Avatar Video",
        "vid_select_resolution": "  Select resolution:",
        "vid_select_aspect_ratio": "  Select aspect ratio:",
        "vid_select_duration": "  Select duration:",
        "vid_resolution_label": "  Resolution    {res}",
        "vid_aspect_ratio_label": "  Aspect ratio  {ar}",
        "vid_duration_label": "  Duration       {dur} sec",
        "vid_cost_label": "  Cost              <b>{coins} coins</b>",
        "vid_cost_label_short": "  Cost   <b>{coins} coins</b>",
        "vid_audio_label": "  Audio            {audio}",
        "vid_audio_yes": "Yes",
        "vid_audio_no": "No",
        "vid_include_audio": "  Include audio in the video?",
        "vid_btn_with_audio": "🔊  With Audio",
        "vid_btn_no_audio": "🔇  No Audio",
        "vid_enter_prompt": "Enter your prompt:",
        "vid_btn_confirm": "◈  Confirm  ({coins} coins)",
        "vid_btn_edit_prompt": "✎  Edit Prompt",
        "vid_edit_prompt_prompt": "✎  Enter your new prompt:",
        "vid_order_summary_title": "◈  <b>Order Summary</b>",
        "vid_model_label": "  Model          <b>{name}</b>",
        "vid_language_label": "  Language      {lang}",
        "vid_attachments_label": "\n  Attachments:\n",
        "vid_prompt_label": "  Prompt:",
        "vid_session_expired": "Session expired. Please start your order again.",
        "vid_insufficient_coins": "Insufficient coins. Please top up your wallet.",
        "vid_order_placed_title": "◌  <b>Order #{oid} Placed</b>",
        "vid_model_row": "  Model     <b>{name}</b>",
        "vid_coins_deducted": "  Coins      <b>{coins} deducted</b>",
        "vid_estimated_delivery": "  Estimated delivery  ~2 minutes",
        "vid_will_deliver": "  Your result will be sent here.",

        "vid_extend_title": "◈  <b>Veo 3.1 Extend Video</b>",
        "vid_extend_desc": "  Extend any video clip by 7 seconds.\n\n  Select mode:",
        "vid_extend_fast": "Fast  —  14◈  (7 sec)",
        "vid_extend_premium": "Premium  —  30◈  (7 sec)",

        "vid_grok_title": "◈  <b>Grok Imagine 1.5</b>",
        "vid_grok_resolution_line": "  Resolution: 720p\n\n  Select duration:",

        "vid_unknown_tool_alert": "Unknown tool",
        "vid_select_lang_label": "◈  Select target language:",
        "vid_translate_cost": "  Cost   <b>{coins} coins</b>",
        "vid_send_video_any_format": "  Send your video file in any format\n  (MP4, MOV, AVI, MKV etc.)",
        "vid_please_send_video": "Please send a video file (MP4, MOV, AVI, MKV etc.)\n\nType /cancel to exit.",
        "vid_video_received": "✓  Video received",
        "vid_add_notes_prompt": "  Add any additional notes (optional)\n  or skip to confirm order:",
        "vid_btn_add_notes": "✎  Add Notes",
        "vid_add_notes_only": "✎  Add notes or instructions (optional):",

        "vid_attach_start_frame": "  ◈  Start frame\n",
        "vid_attach_end_frame": "  ◈  End frame\n",
        "vid_attach_imgs": "  ◈  {count} image ref(s)\n",
        "vid_attach_vids": "  ◈  {count} video ref(s)\n",
        "vid_attach_auds": "  ◈  {count} audio file(s)\n",

        "vid_attach_optional_inline": "Attach reference files (optional)\n  or skip directly to your prompt.",
        "vid_sd_attach_warning": (
            "  ⚠️  Start/End Frame cannot be combined\n"
            "  with other attachment types."
        ),
        "vid_btn_start_frame": "Start Frame",
        "vid_btn_end_frame": "End Frame",
        "vid_btn_clear_startend": "✕  Clear Start/End",
        "vid_btn_clear": "✕  Clear",
        "vid_btn_image_ref": "◈  Image Ref  ({count}/{max})",
        "vid_btn_image_reference": "◈  Image Reference",
        "vid_btn_image_reference_max": "◈  Image Reference  (up to {max})",
        "vid_btn_video_ref": "◈  Video Ref  ({count}/{max})",
        "vid_btn_video_reference": "◈  Video Reference",
        "vid_btn_video_reference_max": "◈  Video Reference  (up to {max}){req}",
        "vid_btn_audio_file": "◈  Audio File  ({count}/{max})",
        "vid_btn_audio_file_plain": "◈  Audio File",
        "vid_btn_audio_file_max": "◈  Audio File  (up to {max})",
        "vid_btn_start_end_frame": "◈  Start & End Frame",
        "vid_btn_start_frame_only": "◈  Start Frame",
        "vid_required_label": " *required",
        "vid_btn_write_prompt": "✓  Write Prompt →",
        "vid_btn_skip_write_prompt": "▸  Skip — Write Prompt",
        "vid_btn_confirm_order": "◈  Confirm Order",
        "vid_btn_upload_required": "⚠️  Upload {items} to continue",
        "vid_required_and": " & ",
        "vid_required_video": "video",
        "vid_required_image": "image",
        "vid_required_audio": "audio",
        "vid_required_start_frame": "start frame",
        "vid_required_files_alert": "Please upload required files: {items}",
        "vid_required_files_alert_simple": "Please upload the required files first.",

        "vid_start_frame_title": "◈  <b>Start Frame</b>",
        "vid_start_frame_desc": "  Send the image for the <b>first frame</b> of your video.\n\n  Reference it in your prompt as <code>@start</code>",
        "vid_start_frame_desc_short": "  Send the image for the <b>first frame</b>.\n\n  Reference it in your prompt as <code>@start</code>",
        "vid_end_frame_title": "◈  <b>End Frame</b>",
        "vid_end_frame_desc": "  Send the image for the <b>last frame</b> of your video.\n\n  Reference it in your prompt as <code>@end</code>",
        "vid_end_frame_desc_short": "  Send the image for the <b>last frame</b>.\n\n  Reference it in your prompt as <code>@end</code>",
        "vid_please_send_image": "◈  Please send an image file (JPG, PNG, WEBP etc.)",
        "vid_please_send_video_short": "◈  Please send a video file (MP4, MOV, AVI etc.)",
        "vid_please_send_audio": "◈  Please send an audio file (MP3, OGG, WAV, M4A etc.)",
        "vid_start_frame_saved": "✓  Start frame saved.\n\nNow set the End Frame or write your prompt.",
        "vid_end_frame_saved": "✓  End frame saved.\n\nWrite your prompt when ready.",

        "vid_img_ref_title": "◈  <b>Image Reference</b>  ({count}/{max})",
        "vid_img_ref_instructions": (
            "  Send up to <b>{max} images</b> as reference.\n\n"
            "  <code>@img1</code>, <code>@img2</code> etc. are just labels\n"
            "  for you — the AI doesn't read them. Describe each image\n"
            "  in words in your prompt instead (e.g. \"the woman in photo 1\").\n\n"
            "  Send images one by one or as album.\n"
            "  Tap <b>Done</b> when finished."
        ),
        "vid_img_ref_instructions_short": (
            "  Send up to <b>{max} image(s)</b>.\n"
            "  <code>@img1</code> etc. are just labels for you — the AI\n"
            "  doesn't read them. Describe each image in words instead.\n\n"
            "  Tap Done when finished."
        ),
        "vid_img_max_reached": "Maximum {max} images reached. Tap Done to continue.",
        "vid_img_max_reached_short": "Maximum {max} image(s) reached. Tap Done.",
        "vid_img_saved": "✓  Image @img{n} saved.  ({count}/{max})",
        "vid_img_saved_short": "✓  @img{n} saved  ({count}/{max})",
        "vid_send_more_or_done": "Send more or tap Done.",
        "vid_max_reached_tap_done": "Maximum reached. Tap Done.",

        "vid_vid_ref_title": "◈  <b>Video Reference</b>  ({count}/{max})",
        "vid_vid_ref_instructions": (
            "  Send up to <b>{max} videos</b> as reference.\n\n"
            "  <code>@vid1</code>, <code>@vid2</code> etc. are just labels\n"
            "  for you — the AI doesn't read them. Describe each video\n"
            "  in words in your prompt instead.\n\n"
            "  Tap <b>Done</b> when finished."
        ),
        "vid_vid_ref_instructions_short": (
            "  Send up to <b>{max} video(s)</b> in any format.\n"
            "  <code>@vid1</code> etc. are just labels for you — the AI\n"
            "  doesn't read them. Describe each video in words instead.\n\n"
            "  Tap Done when finished."
        ),
        "vid_vid_max_reached": "Maximum {max} videos reached. Tap Done to continue.",
        "vid_vid_max_reached_short": "Maximum {max} video(s) reached. Tap Done.",
        "vid_vid_saved": "✓  Video @vid{n} saved.  ({count}/{max})",
        "vid_vid_saved_short": "✓  @vid{n} saved  ({count}/{max})",

        "vid_aud_ref_title": "◈  <b>Audio File</b>  ({count}/{max})",
        "vid_aud_ref_instructions": (
            "  Send up to <b>{max} audio files</b>.\n\n"
            "  <code>@aud1</code>, <code>@aud2</code> etc. are just labels\n"
            "  for you — the AI doesn't read them. Describe each audio\n"
            "  file in words in your prompt instead.\n\n"
            "  Tap <b>Done</b> when finished."
        ),
        "vid_aud_ref_instructions_short": (
            "  Send up to <b>{max} audio file(s)</b>.\n"
            "  <code>@aud1</code> etc. are just labels for you — the AI\n"
            "  doesn't read them. Describe each audio file in words instead.\n\n"
            "  Tap Done when finished."
        ),
        "vid_aud_max_reached": "Maximum {max} audio files reached. Tap Done to continue.",
        "vid_aud_max_reached_short": "Maximum {max} audio file(s) reached. Tap Done.",
        "vid_aud_saved": "✓  Audio @aud{n} saved.  ({count}/{max})",
        "vid_aud_saved_short": "✓  @aud{n} saved  ({count}/{max})",

        "vid_attached_files_label": "\n  <b>Attached files:</b>\n{lines}\n  Note: these labels are just for your own reference —\n  the AI doesn't read them. Describe each file in words\n  in your prompt.\n",
        "vid_attach_n_imgs": "  ◈  {count} image(s) → @img1",
        "vid_attach_n_vids": "  ◈  {count} video(s) → @vid1",
        "vid_attach_n_auds": "  ◈  {count} audio(s) → @aud1",
        "vid_attach_start_attached": "  ◈  Start frame attached\n",
        "vid_attach_end_attached": "  ◈  End frame attached\n",
        "vid_now_select_resolution": "  Now select resolution:",

        "vid_hgtr_quality_desc": (
            "  Select quality mode:\n\n"
            "  <b>Precision</b>  —  highest accuracy, slower\n"
            "  <b>Speed</b>  —  faster processing, lower cost"
        ),
        "vid_btn_precision": "◈  Precision",
        "vid_btn_speed": "◈  Speed",

        "vid_hga4_select_ar": "  Select aspect ratio:",
        "vid_hga4_select_res": "  Select resolution:",
        "vid_hga4_select_style": "  Select talking style:",
        "vid_omni_desc": "  Animate any portrait with voice.\n\n  Select duration:",

        # ── Wallet / top-up flow ────────────────────────────────
        "wallet_title": "◈  <b>Your Wallet</b>",
        "wallet_balance": "  Balance     <b>{coins} coins</b>  (≈ ${usd})",
        "wallet_rate": "  Rate          1 coin  =  $0.05",
        "wallet_min_topup": "  Min top-up   $2.00  =  40 coins",
        "wallet_btn_add_coins": "＋  Add Coins",
        "wallet_btn_referral": "◈  Referral Program",

        "wallet_topup_title": "＋  <b>Add Coins</b>",
        "wallet_topup_rate_line": "  1 coin  =  <b>$0.05</b>",
        "wallet_topup_min_line": "  $2.00   =  <b>40 coins</b>  ← minimum",
        "wallet_topup_5_line": "  $5.00   =  <b>100 coins</b>",
        "wallet_topup_10_line": "  $10.00  =  <b>200 coins</b>",
        "wallet_topup_select_or_custom": "Select amount or enter custom:",
        "wallet_btn_2": "$2  →  40 coins",
        "wallet_btn_5": "$5  →  100 coins",
        "wallet_btn_10": "$10  →  200 coins",
        "wallet_btn_20": "$20  →  400 coins",
        "wallet_btn_custom": "✎  Custom amount",

        "wallet_custom_title": "✎  <b>Custom Amount</b>",
        "wallet_custom_desc": "Type the amount in USD (minimum $2.00):\n\n<i>Example: 7.5</i>",
        "wallet_min_deposit_error": "Minimum deposit is ${min}. Please enter a valid amount (e.g. 2, 5, 10).",
        "wallet_enter_number_error": "Please enter a number (e.g. 5 or 7.50).\n\nType /cancel to exit.",

        "wallet_confirm_title": "◈  <b>Confirm Top-up</b>",
        "wallet_confirm_amount": "  Amount      <b>${amount}</b>",
        "wallet_confirm_receive": "  You receive  <b>{coins} coins</b>",
        "wallet_choose_payment": "Choose payment method:",
        "wallet_btn_pay_stars": "⭐  Pay with Stars ({stars} XTR)",
        "wallet_btn_pay_usdt": "₮  Pay with USDT (TRC20)",

        "wallet_usdt_title": "₮  <b>USDT Payment</b>",
        "wallet_usdt_send_exactly": "  Send exactly  <b>${amount} USDT</b>",
        "wallet_usdt_network": "  Network          <b>TRC20 (Tron)</b>",
        "wallet_usdt_address_label": "  Wallet address:",
        "wallet_usdt_after_sending": "After sending, paste your <b>transaction hash</b> below.\n<i>The system will verify it automatically.</i>",

        "wallet_verifying": "⏳  Verifying transaction...",
        "wallet_verified_title": "✓  <b>Payment Verified</b>",
        "wallet_verified_confirmed": "  Transaction confirmed",
        "wallet_verified_amount": "  Amount received   <b>${amount} USDT</b>",
        "wallet_verified_coins": "  Coins credited     <b>{coins} coins</b>",
        "wallet_verified_balance": "  New balance        <b>{coins} coins</b>",

        "wallet_review_title": "◌  <b>Under Review</b>",
        "wallet_review_body": (
            "  We could not verify your transaction automatically.\n"
            "  Our team will review it manually within 15 minutes.\n\n"
            "  Coins will be credited after confirmation."
        ),

        "wallet_stars_invoice_title": "RetainX Studio — Coins",
        "wallet_stars_invoice_desc": "Top up {coins} coins to your RetainX account",
        "wallet_stars_label": "{coins} Coins",
        "wallet_stars_success_title": "⭐  <b>Payment Successful</b>",
        "wallet_stars_success_body": "  {coins} coins added to your wallet.\n  New balance: <b>{coins2} coins</b>",

        "wallet_topup_confirmed_title": "✓  <b>Top-up Confirmed</b>",
        "wallet_topup_confirmed_body": "  <b>{coins} coins</b> added to your wallet.\n  Balance: <b>{balance} coins</b>",
        "wallet_topup_rejected": "✕  Your top-up was not confirmed. Please contact support.",

        "wallet_referral_bonus_title": "◈  <b>Referral Bonus</b>",
        "wallet_referral_bonus_body": "  Your referral topped up their wallet.\n  You received <b>{bonus} coins</b> (20%).",

        "wallet_referral_title": "◈  <b>Referral Program</b>",
        "wallet_referral_desc": "  Earn <b>20% in coins</b> every time your referral tops up.",
        "wallet_referral_link_label": "  Your referral link:",
        "wallet_referral_share": "  Share it and earn passively.",

        # ── Order history flow ──────────────────────────────────
        "order_history_title": "◈  <b>Order History</b>",
        "order_history_empty": "  You have no orders yet.\n\n  Start generating to see your history here.",
        "order_history_total": "  Total orders    <b>{total}</b>",
        "order_history_completed": "  Completed       <b>{delivered}</b>",
        "order_history_spent": "  Coins spent     <b>{spent}◈</b>",
        "order_history_tap_to_view": "  Tap any order to view details:",
        "order_not_found": "Order not found",
        "order_detail_title": "◈  <b>Order #{oid}</b>",
        "order_detail_status": "  Status    {emoji}  <b>{status}</b>",
        "order_detail_model": "  Model     <b>{tool}</b>",
        "order_detail_coins": "  Coins      {coins}◈",
        "order_detail_date": "  Date        {date}",
        "order_detail_resolution": "  Resolution    {res}",
        "order_detail_aspect_ratio": "  Aspect ratio  {ar}",
        "order_detail_duration": "  Duration       {dur} sec",
        "order_detail_quality": "  Quality          {quality}",
        "order_detail_audio": "  Audio            Yes",
        "order_detail_language": "  Language      {lang}",
        "order_detail_prompt_label": "  Prompt:",
        "order_btn_repeat": "↺  Repeat this order",
        "order_btn_back": "← Back",
        "order_repeat_title": "◈  <b>Repeat Order</b>",
        "order_repeat_model": "  Model     <b>{tool}</b>",
        "order_repeat_resolution": "  Resolution   {res}",
        "order_repeat_aspect": "  Aspect        {ar}",
        "order_repeat_duration": "  Duration      {dur} sec",
        "order_repeat_cost": "  Cost           <b>{coins} coins</b>",
        "order_repeat_prev_prompt": "  Previous prompt:",
        "order_repeat_enter_prompt": "  Enter your prompt (or send same as above):",
        "order_status_processing": "Processing",
        "order_status_delivered": "Delivered",
        "order_status_cancelled": "Cancelled",
        "order_your_result": "◈  Your generated result",
    },
    "ru": {
        "welcome_title": "◈  <b>Добро пожаловать в RetainX Studio</b>",
        "welcome_body": (
            "  Самый быстрый и доступный способ\n"
            "  генерации AI видео, изображений и аудио.\n\n"
            "  ◉  Kling 3.0  ·  Veo 3.1  ·  Sora 2\n"
            "  ◉  Midjourney  ·  Flux  ·  Seedance\n"
            "  ◉  HeyGen  ·  ElevenLabs  ·  LTX\n\n"
            "  До <b>3× дешевле</b> любого конкурента.\n"
            "  Результат за <b>~2 минуты.</b>"
        ),
        "welcome_bonus": "  🎁  <b>{bonus} монет</b> начислено на ваш счёт.\n  Баланс   <b>{coins} монет</b>",
        "what_create": "Что бы вы хотели создать?",
        "choose_option": "Выберите вариант:",

        "main_menu_title": "◈  <b>RetainX Studio</b>",
        "main_menu_balance": "  Баланс   <b>{coins} монет</b>",
        "main_menu_desc": "  Генерация AI видео, изображений и аудио\n  по самым выгодным ценам.",

        "btn_video_generation": "▸  Генерация видео",
        "btn_image_generation": "▸  Генерация изображений",
        "btn_audio_voice": "▸  Аудио и голос",
        "btn_wallet_coins": "◈  Кошелёк  ·  {coins} монет",
        "btn_pricing": "◎  Цены",
        "btn_support": "◌  Поддержка",
        "btn_language": "◐  Язык",
        "btn_start_generating": "▸  Начать генерацию",
        "btn_view_pricing": "◎  Смотреть цены",
        "btn_back": "←  Назад",

        "audio_title": "◌  <b>Аудио и голос</b>",
        "audio_body": "  Скоро будет доступно.\n\n  Мы интегрируем инструменты синтеза\n  речи и генерации музыки.\n\n  Следите за обновлениями.",

        "support_title": "◌  <b>Поддержка</b>",
        "support_body": "  Свяжитесь с нами: @RetainXStudio",

        "video_title": "◈  <b>Генерация видео</b>",
        "select_category": "Выберите категорию:",

        "images_title": "◈  <b>Генерация изображений</b>",
        "select_model": "Выберите модель:",

        "pricing_title": "◎  <b>Цены</b>",
        "pricing_body": "  1 монета  =  <b>$0.05</b>\n\n  Выберите категорию для просмотра цен:",
        "btn_image_pricing": "▸  Цены на изображения",
        "btn_video_pricing": "▸  Цены на видео",

        "menu_main_menu": "⌂  Главное меню",
        "menu_wallet": "◈  Кошелёк",
        "menu_video": "▸  Видео",
        "menu_images": "▸  Изображения",
        "menu_audio": "▸  Аудио",
        "menu_orders": "≡  Заказы",
        "menu_support": "◌  Поддержка",

        "lang_title": "◐  <b>Язык</b>",
        "lang_desc": "  Выберите предпочитаемый язык:",
        "lang_changed": "✓  Язык обновлён.",

        "coins_word": "монет",

        # ── Image generation flow ──────────────────────────────
        "img_menu_title": "◈  <b>Генерация изображений</b>",
        "img_menu_select": "Выберите модель, чтобы продолжить:",
        "img_price_label": "Цена",
        "img_per_gen": "за генерацию",
        "img_select_ar": "Выберите соотношение сторон:",
        "img_select_quality": "Выберите качество:",
        "img_aspect_ratio_label": "Соотношение сторон",
        "img_quality_label": "Качество",
        "img_cost_label": "Стоимость",
        "img_balance_label": "Ваш баланс",
        "img_attach_optional": "  Прикрепите референс-изображения (необязательно)\n  или пропустите и напишите промпт.",
        "img_btn_add_ref": "◈  Добавить референс  (до {max})",
        "img_btn_skip_prompt": "▸  Пропустить — написать промпт",
        "img_enter_prompt": "Введите промпт:",
        "img_order_summary_title": "◈  <b>Сводка заказа</b>",
        "img_model_label": "Модель",
        "img_prompt_label": "Промпт:",
        "img_btn_confirm": "◈  Подтвердить  ({coins} монет)",
        "img_btn_edit_prompt": "✎  Изменить промпт",
        "img_edit_prompt_prompt": "✎  Введите новый промпт:",
        "img_session_expired": "Сессия истекла. Начните оформление заказа заново.",
        "img_insufficient_coins": "Недостаточно монет. Пополните кошелёк.",
        "img_order_placed_title": "◌  <b>Заказ #{oid} оформлен</b>",
        "img_model_row": "  Модель     <b>{name}</b>",
        "img_coins_deducted": "  Монеты      <b>{coins} списано</b>",
        "img_estimated_time": "  Ожидаемое время  ~2 минуты",
        "img_will_deliver": "  Мы пришлём изображение сюда в ближайшее время.",
        "img_ref_title": "◈  <b>Референс-изображение</b>  ({count}/{max})",
        "img_ref_instructions": (
            "  Отправьте до <b>{max} изображений</b> в качестве референса.\n\n"
            "  <code>@img1</code>, <code>@img2</code> и т.д. — это просто метки\n"
            "  для вас, ИИ их не считывает. Опишите каждое изображение\n"
            "  словами в промпте.\n\n"
            "  Нажмите <b>Готово</b>, когда закончите."
        ),
        "btn_done": "✓  Готово",
        "img_ref_saved": "✓  Изображение @img{n} сохранено.  ({count}/{max})",
        "img_ref_send_more": "Отправьте ещё или нажмите Готово.",
        "img_ref_max_reached": "Достигнут максимум. Нажмите Готово.",
        "img_ref_max_alert": "Достигнут максимум {max} изображений. Нажмите Готово, чтобы продолжить.",
        "img_refs_attached": "  ◈  {count} референс(ов) прикреплено\n",

        # ── Video generation flow ──────────────────────────────
        "vid_menu_title": "◈  <b>Генерация видео</b>",
        "vid_select_category": "Выберите категорию:",
        "vid_sub_standard": "▸  Стандартное видео",
        "vid_sub_premium": "▸  Премиум видео",
        "vid_sub_kling": "▸  Kling видео",
        "vid_sub_avatar": "▸  Аватары и дубляж",
        "vid_select_model": "Выберите модель:",
        "vid_unknown_tool": "Инструмент не найден",
        "vid_resolution_word": "Разрешение",
        "vid_duration_word": "Длительность",
        "vid_sec_word": "сек",
        "vid_type_word": "Тип",
        "vid_avatar_video_word": "Видео-аватар",
        "vid_select_resolution": "  Выберите разрешение:",
        "vid_select_aspect_ratio": "  Выберите соотношение сторон:",
        "vid_select_duration": "  Выберите длительность:",
        "vid_resolution_label": "  Разрешение    {res}",
        "vid_aspect_ratio_label": "  Соотношение сторон  {ar}",
        "vid_duration_label": "  Длительность   {dur} сек",
        "vid_cost_label": "  Стоимость       <b>{coins} монет</b>",
        "vid_cost_label_short": "  Стоимость   <b>{coins} монет</b>",
        "vid_audio_label": "  Аудио            {audio}",
        "vid_audio_yes": "Да",
        "vid_audio_no": "Нет",
        "vid_include_audio": "  Добавить аудио в видео?",
        "vid_btn_with_audio": "🔊  С аудио",
        "vid_btn_no_audio": "🔇  Без аудио",
        "vid_enter_prompt": "Введите промпт:",
        "vid_btn_confirm": "◈  Подтвердить  ({coins} монет)",
        "vid_btn_edit_prompt": "✎  Изменить промпт",
        "vid_edit_prompt_prompt": "✎  Введите новый промпт:",
        "vid_order_summary_title": "◈  <b>Сводка заказа</b>",
        "vid_model_label": "  Модель          <b>{name}</b>",
        "vid_language_label": "  Язык             {lang}",
        "vid_attachments_label": "\n  Вложения:\n",
        "vid_prompt_label": "  Промпт:",
        "vid_session_expired": "Сессия истекла. Начните оформление заказа заново.",
        "vid_insufficient_coins": "Недостаточно монет. Пополните кошелёк.",
        "vid_order_placed_title": "◌  <b>Заказ #{oid} оформлен</b>",
        "vid_model_row": "  Модель     <b>{name}</b>",
        "vid_coins_deducted": "  Монеты      <b>{coins} списано</b>",
        "vid_estimated_delivery": "  Ожидаемое время  ~2 минуты",
        "vid_will_deliver": "  Результат будет отправлен сюда.",

        "vid_extend_title": "◈  <b>Veo 3.1 Extend Video</b>",
        "vid_extend_desc": "  Продлите любой видеоклип на 7 секунд.\n\n  Выберите режим:",
        "vid_extend_fast": "Fast  —  14◈  (7 сек)",
        "vid_extend_premium": "Premium  —  30◈  (7 сек)",

        "vid_grok_title": "◈  <b>Grok Imagine 1.5</b>",
        "vid_grok_resolution_line": "  Разрешение: 720p\n\n  Выберите длительность:",

        "vid_unknown_tool_alert": "Неизвестный инструмент",
        "vid_select_lang_label": "◈  Выберите целевой язык:",
        "vid_translate_cost": "  Стоимость   <b>{coins} монет</b>",
        "vid_send_video_any_format": "  Отправьте видеофайл в любом формате\n  (MP4, MOV, AVI, MKV и т.д.)",
        "vid_please_send_video": "Отправьте видеофайл (MP4, MOV, AVI, MKV и т.д.)\n\nВведите /cancel для отмены.",
        "vid_video_received": "✓  Видео получено",
        "vid_add_notes_prompt": "  Добавьте примечания (необязательно)\n  или пропустите и подтвердите заказ:",
        "vid_btn_add_notes": "✎  Добавить примечание",
        "vid_add_notes_only": "✎  Добавьте примечания или инструкции (необязательно):",

        "vid_attach_start_frame": "  ◈  Стартовый кадр\n",
        "vid_attach_end_frame": "  ◈  Финальный кадр\n",
        "vid_attach_imgs": "  ◈  {count} референс(ов)-изображений\n",
        "vid_attach_vids": "  ◈  {count} референс(ов)-видео\n",
        "vid_attach_auds": "  ◈  {count} аудиофайл(ов)\n",

        "vid_attach_optional_inline": "Прикрепите референс-файлы (необязательно)\n  или сразу переходите к промпту.",
        "vid_sd_attach_warning": (
            "  ⚠️  Стартовый/финальный кадр нельзя сочетать\n"
            "  с другими типами вложений."
        ),
        "vid_btn_start_frame": "Стартовый кадр",
        "vid_btn_end_frame": "Финальный кадр",
        "vid_btn_clear_startend": "✕  Очистить старт/финал",
        "vid_btn_clear": "✕  Очистить",
        "vid_btn_image_ref": "◈  Референс-изображение  ({count}/{max})",
        "vid_btn_image_reference": "◈  Референс-изображение",
        "vid_btn_image_reference_max": "◈  Референс-изображение  (до {max})",
        "vid_btn_video_ref": "◈  Референс-видео  ({count}/{max})",
        "vid_btn_video_reference": "◈  Референс-видео",
        "vid_btn_video_reference_max": "◈  Референс-видео  (до {max}){req}",
        "vid_btn_audio_file": "◈  Аудиофайл  ({count}/{max})",
        "vid_btn_audio_file_plain": "◈  Аудиофайл",
        "vid_btn_audio_file_max": "◈  Аудиофайл  (до {max})",
        "vid_btn_start_end_frame": "◈  Стартовый и финальный кадр",
        "vid_btn_start_frame_only": "◈  Стартовый кадр",
        "vid_required_label": " *обязательно",
        "vid_btn_write_prompt": "✓  Написать промпт →",
        "vid_btn_skip_write_prompt": "▸  Пропустить — написать промпт",
        "vid_btn_confirm_order": "◈  Подтвердить заказ",
        "vid_btn_upload_required": "⚠️  Загрузите {items}, чтобы продолжить",
        "vid_required_and": " и ",
        "vid_required_video": "видео",
        "vid_required_image": "изображение",
        "vid_required_audio": "аудио",
        "vid_required_start_frame": "стартовый кадр",
        "vid_required_files_alert": "Загрузите необходимые файлы: {items}",
        "vid_required_files_alert_simple": "Сначала загрузите необходимые файлы.",

        "vid_start_frame_title": "◈  <b>Стартовый кадр</b>",
        "vid_start_frame_desc": "  Отправьте изображение для <b>первого кадра</b> видео.\n\n  Указывайте его в промпте как <code>@start</code>",
        "vid_start_frame_desc_short": "  Отправьте изображение для <b>первого кадра</b>.\n\n  Указывайте его в промпте как <code>@start</code>",
        "vid_end_frame_title": "◈  <b>Финальный кадр</b>",
        "vid_end_frame_desc": "  Отправьте изображение для <b>последнего кадра</b> видео.\n\n  Указывайте его в промпте как <code>@end</code>",
        "vid_end_frame_desc_short": "  Отправьте изображение для <b>последнего кадра</b>.\n\n  Указывайте его в промпте как <code>@end</code>",
        "vid_please_send_image": "◈  Отправьте файл изображения (JPG, PNG, WEBP и т.д.)",
        "vid_please_send_video_short": "◈  Отправьте видеофайл (MP4, MOV, AVI и т.д.)",
        "vid_please_send_audio": "◈  Отправьте аудиофайл (MP3, OGG, WAV, M4A и т.д.)",
        "vid_start_frame_saved": "✓  Стартовый кадр сохранён.\n\nТеперь укажите финальный кадр или напишите промпт.",
        "vid_end_frame_saved": "✓  Финальный кадр сохранён.\n\nНапишите промпт, когда будете готовы.",

        "vid_img_ref_title": "◈  <b>Референс-изображение</b>  ({count}/{max})",
        "vid_img_ref_instructions": (
            "  Отправьте до <b>{max} изображений</b> в качестве референса.\n\n"
            "  <code>@img1</code>, <code>@img2</code> и т.д. — это просто метки\n"
            "  для вас, ИИ их не считывает. Опишите каждое изображение\n"
            "  словами в промпте (например, «женщина на фото 1»).\n\n"
            "  Отправляйте изображения по одному или альбомом.\n"
            "  Нажмите <b>Готово</b>, когда закончите."
        ),
        "vid_img_ref_instructions_short": (
            "  Отправьте до <b>{max} изображения(ий)</b>.\n"
            "  <code>@img1</code> и т.д. — это просто метки для вас, ИИ\n"
            "  их не считывает. Опишите каждое изображение словами.\n\n"
            "  Нажмите Готово, когда закончите."
        ),
        "vid_img_max_reached": "Достигнут максимум {max} изображений. Нажмите Готово, чтобы продолжить.",
        "vid_img_max_reached_short": "Достигнут максимум {max} изображения(ий). Нажмите Готово.",
        "vid_img_saved": "✓  Изображение @img{n} сохранено.  ({count}/{max})",
        "vid_img_saved_short": "✓  @img{n} сохранено  ({count}/{max})",
        "vid_send_more_or_done": "Отправьте ещё или нажмите Готово.",
        "vid_max_reached_tap_done": "Достигнут максимум. Нажмите Готово.",

        "vid_vid_ref_title": "◈  <b>Референс-видео</b>  ({count}/{max})",
        "vid_vid_ref_instructions": (
            "  Отправьте до <b>{max} видео</b> в качестве референса.\n\n"
            "  <code>@vid1</code>, <code>@vid2</code> и т.д. — это просто метки\n"
            "  для вас, ИИ их не считывает. Опишите каждое видео\n"
            "  словами в промпте.\n\n"
            "  Нажмите <b>Готово</b>, когда закончите."
        ),
        "vid_vid_ref_instructions_short": (
            "  Отправьте до <b>{max} видео</b> в любом формате.\n"
            "  <code>@vid1</code> и т.д. — это просто метки для вас, ИИ\n"
            "  их не считывает. Опишите каждое видео словами.\n\n"
            "  Нажмите Готово, когда закончите."
        ),
        "vid_vid_max_reached": "Достигнут максимум {max} видео. Нажмите Готово, чтобы продолжить.",
        "vid_vid_max_reached_short": "Достигнут максимум {max} видео. Нажмите Готово.",
        "vid_vid_saved": "✓  Видео @vid{n} сохранено.  ({count}/{max})",
        "vid_vid_saved_short": "✓  @vid{n} сохранено  ({count}/{max})",

        "vid_aud_ref_title": "◈  <b>Аудиофайл</b>  ({count}/{max})",
        "vid_aud_ref_instructions": (
            "  Отправьте до <b>{max} аудиофайлов</b>.\n\n"
            "  <code>@aud1</code>, <code>@aud2</code> и т.д. — это просто метки\n"
            "  для вас, ИИ их не считывает. Опишите каждый аудиофайл\n"
            "  словами в промпте.\n\n"
            "  Нажмите <b>Готово</b>, когда закончите."
        ),
        "vid_aud_ref_instructions_short": (
            "  Отправьте до <b>{max} аудиофайла(ов)</b>.\n"
            "  <code>@aud1</code> и т.д. — это просто метки для вас, ИИ\n"
            "  их не считывает. Опишите каждый аудиофайл словами.\n\n"
            "  Нажмите Готово, когда закончите."
        ),
        "vid_aud_max_reached": "Достигнут максимум {max} аудиофайлов. Нажмите Готово, чтобы продолжить.",
        "vid_aud_max_reached_short": "Достигнут максимум {max} аудиофайла(ов). Нажмите Готово.",
        "vid_aud_saved": "✓  Аудио @aud{n} сохранено.  ({count}/{max})",
        "vid_aud_saved_short": "✓  @aud{n} сохранено  ({count}/{max})",

        "vid_attached_files_label": "\n  <b>Прикреплённые файлы:</b>\n{lines}\n  Примечание: эти метки нужны только для вас —\n  ИИ их не считывает. Опишите каждый файл словами\n  в промпте.\n",
        "vid_attach_n_imgs": "  ◈  {count} изображение(й) → @img1",
        "vid_attach_n_vids": "  ◈  {count} видео → @vid1",
        "vid_attach_n_auds": "  ◈  {count} аудио → @aud1",
        "vid_attach_start_attached": "  ◈  Стартовый кадр прикреплён\n",
        "vid_attach_end_attached": "  ◈  Финальный кадр прикреплён\n",
        "vid_now_select_resolution": "  Теперь выберите разрешение:",

        "vid_hgtr_quality_desc": (
            "  Выберите режим качества:\n\n"
            "  <b>Precision</b>  —  максимальная точность, медленнее\n"
            "  <b>Speed</b>  —  быстрее, дешевле"
        ),
        "vid_btn_precision": "◈  Precision",
        "vid_btn_speed": "◈  Speed",

        "vid_hga4_select_ar": "  Выберите соотношение сторон:",
        "vid_hga4_select_res": "  Выберите разрешение:",
        "vid_hga4_select_style": "  Выберите стиль речи:",
        "vid_omni_desc": "  Анимируйте любой портрет с озвучкой.\n\n  Выберите длительность:",

        # ── Wallet / top-up flow ────────────────────────────────
        "wallet_title": "◈  <b>Ваш кошелёк</b>",
        "wallet_balance": "  Баланс       <b>{coins} монет</b>  (≈ ${usd})",
        "wallet_rate": "  Курс           1 монета  =  $0.05",
        "wallet_min_topup": "  Мин. пополнение   $2.00  =  40 монет",
        "wallet_btn_add_coins": "＋  Пополнить",
        "wallet_btn_referral": "◈  Реферальная программа",

        "wallet_topup_title": "＋  <b>Пополнение</b>",
        "wallet_topup_rate_line": "  1 монета  =  <b>$0.05</b>",
        "wallet_topup_min_line": "  $2.00   =  <b>40 монет</b>  ← минимум",
        "wallet_topup_5_line": "  $5.00   =  <b>100 монет</b>",
        "wallet_topup_10_line": "  $10.00  =  <b>200 монет</b>",
        "wallet_topup_select_or_custom": "Выберите сумму или введите свою:",
        "wallet_btn_2": "$2  →  40 монет",
        "wallet_btn_5": "$5  →  100 монет",
        "wallet_btn_10": "$10  →  200 монет",
        "wallet_btn_20": "$20  →  400 монет",
        "wallet_btn_custom": "✎  Своя сумма",

        "wallet_custom_title": "✎  <b>Своя сумма</b>",
        "wallet_custom_desc": "Введите сумму в USD (минимум $2.00):\n\n<i>Пример: 7.5</i>",
        "wallet_min_deposit_error": "Минимальное пополнение — ${min}. Введите корректную сумму (например, 2, 5, 10).",
        "wallet_enter_number_error": "Введите число (например, 5 или 7.50).\n\nВведите /cancel для отмены.",

        "wallet_confirm_title": "◈  <b>Подтверждение пополнения</b>",
        "wallet_confirm_amount": "  Сумма        <b>${amount}</b>",
        "wallet_confirm_receive": "  Вы получите   <b>{coins} монет</b>",
        "wallet_choose_payment": "Выберите способ оплаты:",
        "wallet_btn_pay_stars": "⭐  Оплатить Stars ({stars} XTR)",
        "wallet_btn_pay_usdt": "₮  Оплатить USDT (TRC20)",

        "wallet_usdt_title": "₮  <b>Оплата USDT</b>",
        "wallet_usdt_send_exactly": "  Отправьте ровно  <b>${amount} USDT</b>",
        "wallet_usdt_network": "  Сеть              <b>TRC20 (Tron)</b>",
        "wallet_usdt_address_label": "  Адрес кошелька:",
        "wallet_usdt_after_sending": "После отправки вставьте <b>хэш транзакции</b> ниже.\n<i>Система проверит его автоматически.</i>",

        "wallet_verifying": "⏳  Проверка транзакции...",
        "wallet_verified_title": "✓  <b>Платёж подтверждён</b>",
        "wallet_verified_confirmed": "  Транзакция подтверждена",
        "wallet_verified_amount": "  Получено   <b>${amount} USDT</b>",
        "wallet_verified_coins": "  Зачислено монет   <b>{coins} монет</b>",
        "wallet_verified_balance": "  Новый баланс       <b>{coins} монет</b>",

        "wallet_review_title": "◌  <b>На проверке</b>",
        "wallet_review_body": (
            "  Не удалось автоматически проверить транзакцию.\n"
            "  Наша команда проверит её вручную в течение 15 минут.\n\n"
            "  Монеты будут зачислены после подтверждения."
        ),

        "wallet_stars_invoice_title": "RetainX Studio — Монеты",
        "wallet_stars_invoice_desc": "Пополнение на {coins} монет для аккаунта RetainX",
        "wallet_stars_label": "{coins} монет",
        "wallet_stars_success_title": "⭐  <b>Платёж успешен</b>",
        "wallet_stars_success_body": "  {coins} монет добавлено на ваш счёт.\n  Новый баланс: <b>{coins2} монет</b>",

        "wallet_topup_confirmed_title": "✓  <b>Пополнение подтверждено</b>",
        "wallet_topup_confirmed_body": "  <b>{coins} монет</b> добавлено на ваш счёт.\n  Баланс: <b>{balance} монет</b>",
        "wallet_topup_rejected": "✕  Ваше пополнение не было подтверждено. Свяжитесь с поддержкой.",

        "wallet_referral_bonus_title": "◈  <b>Реферальный бонус</b>",
        "wallet_referral_bonus_body": "  Ваш реферал пополнил свой кошелёк.\n  Вы получили <b>{bonus} монет</b> (20%).",

        "wallet_referral_title": "◈  <b>Реферальная программа</b>",
        "wallet_referral_desc": "  Получайте <b>20% монетами</b> за каждое пополнение вашего реферала.",
        "wallet_referral_link_label": "  Ваша реферальная ссылка:",
        "wallet_referral_share": "  Поделитесь ей и зарабатывайте пассивно.",

        # ── Order history flow ──────────────────────────────────
        "order_history_title": "◈  <b>История заказов</b>",
        "order_history_empty": "  У вас пока нет заказов.\n\n  Начните генерацию, чтобы увидеть историю здесь.",
        "order_history_total": "  Всего заказов   <b>{total}</b>",
        "order_history_completed": "  Завершено        <b>{delivered}</b>",
        "order_history_spent": "  Потрачено монет  <b>{spent}◈</b>",
        "order_history_tap_to_view": "  Нажмите на заказ, чтобы увидеть детали:",
        "order_not_found": "Заказ не найден",
        "order_detail_title": "◈  <b>Заказ #{oid}</b>",
        "order_detail_status": "  Статус    {emoji}  <b>{status}</b>",
        "order_detail_model": "  Модель     <b>{tool}</b>",
        "order_detail_coins": "  Монеты     {coins}◈",
        "order_detail_date": "  Дата          {date}",
        "order_detail_resolution": "  Разрешение    {res}",
        "order_detail_aspect_ratio": "  Соотношение сторон  {ar}",
        "order_detail_duration": "  Длительность   {dur} сек",
        "order_detail_quality": "  Качество        {quality}",
        "order_detail_audio": "  Аудио            Да",
        "order_detail_language": "  Язык             {lang}",
        "order_detail_prompt_label": "  Промпт:",
        "order_btn_repeat": "↺  Повторить заказ",
        "order_btn_back": "← Назад",
        "order_repeat_title": "◈  <b>Повтор заказа</b>",
        "order_repeat_model": "  Модель     <b>{tool}</b>",
        "order_repeat_resolution": "  Разрешение   {res}",
        "order_repeat_aspect": "  Соотношение   {ar}",
        "order_repeat_duration": "  Длительность  {dur} сек",
        "order_repeat_cost": "  Стоимость      <b>{coins} монет</b>",
        "order_repeat_prev_prompt": "  Предыдущий промпт:",
        "order_repeat_enter_prompt": "  Введите промпт (или отправьте такой же, как выше):",
        "order_status_processing": "В обработке",
        "order_status_delivered": "Доставлен",
        "order_status_cancelled": "Отменён",
        "order_your_result": "◈  Ваш результат",
    },
}


def t(key: str, lang: str = "en", **kwargs) -> str:
    s = STR.get(lang, STR["en"]).get(key, STR["en"].get(key, key))
    return s.format(**kwargs) if kwargs else s


# ── Client reply-keyboard button labels (per language, with reverse lookup) ──
CLIENT_BUTTONS = {
    "main_menu": {"en": STR["en"]["menu_main_menu"], "ru": STR["ru"]["menu_main_menu"]},
    "wallet":    {"en": STR["en"]["menu_wallet"],     "ru": STR["ru"]["menu_wallet"]},
    "video":     {"en": STR["en"]["menu_video"],      "ru": STR["ru"]["menu_video"]},
    "images":    {"en": STR["en"]["menu_images"],     "ru": STR["ru"]["menu_images"]},
    "audio":     {"en": STR["en"]["menu_audio"],      "ru": STR["ru"]["menu_audio"]},
    "orders":    {"en": STR["en"]["menu_orders"],     "ru": STR["ru"]["menu_orders"]},
    "support":   {"en": STR["en"]["menu_support"],    "ru": STR["ru"]["menu_support"]},
}

CLIENT_ACTION_BY_TEXT = {
    label: action
    for action, labels in CLIENT_BUTTONS.items()
    for label in labels.values()
}

CLIENT_TEXTS = set(CLIENT_ACTION_BY_TEXT.keys())
