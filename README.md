# ComfyUI DeepSeek_R1 Chat Node

A custom node for ComfyUI that integrates DeepSeek's powerful chat and instruction API, enabling seamless AI interactions within your ComfyUI workflows.

![image](https://github.com/user-attachments/assets/ea6c65e6-2fde-4450-8c7c-b117efb965b7)

## Features

- **Dual Operating Modes**
  - Chat mode with conversation memory
  - Single-turn instruction mode
  
- **Vision Integration**
  - Support for image context through vision descriptions
  - Seamless integration with ComfyUI's visual workflows

- **Advanced Configuration**
  - Customizable max token limit (up to 8192 tokens)
  - Optional reasoning display
  - Configurable chat history management
  - Built-in rate limiting protection

## Installation

1. Clone this repository into your ComfyUI custom nodes directory:
```bash
cd ComfyUI/custom_nodes
git clone https://github.com/ShmuelRonen/comfyui-deepseek-chat.git
```

2. Get your DeepSeek API key:
   - Go to [platform.deepseek.com/api_keys](https://platform.deepseek.com/)
   - Sign in or create an account
   - Generate a new API key
   - Copy the key

3. Edit the`config.json` file in the node directory:
```json
{
    "deepseek_api_key": "your-api-key-here"
}
```
## Important
**Check API availability on this site**:  [DeepSeek API status]([https://platform.deepseek.com/](https://status-deepseek-com.translate.goog/?_x_tr_sl=auto&_x_tr_tl=en&_x_tr_hl=iw&_x_tr_pto=wapp)

## Usage)) 

### Node Configuration

The node provides several input parameters:

- **mode**: Choose between "chat" and "instruct"
- **prompt**: Your input text/question
- **max_tokens**: Maximum response length (1-8192)
- **show_reasoning**: Toggle reasoning display
- **clear_history**: Option to reset conversation
- **remember_chat**: Enable/disable chat history persistence
- **vision_description**: Optional image context description. This can be used to:
  - Provide image descriptions for visual context
  - Connect with image generation nodes
  - Enable vision-language tasks
  - Process image analysis results

### Example Workflow

1. Add the "DeepSeek-V3 Chat/Instruct" node to your workflow
2. Configure the node parameters
3. Connect it to other nodes as needed
4. Execute the workflow

### Outputs

The node provides two outputs:
- `latest_response`: The most recent AI response
- `full_chat_history`: Complete conversation history

## Rate Limiting

The node implements a 1-second minimum interval between requests to comply with API limits.

## Error Handling

- Comprehensive error logging
- Graceful handling of API failures
- Clear error messages in node outputs

## Technical Details

### API Integration
```
API Endpoint: https://api.deepseek.com/v1/chat/completions
Model: deepseek-reasoner
```
- Supports full chat context with message history
- Handles authentication via API key
- Implements rate limiting protection

### File Structure
```
comfyui-deepseek-chat/
├── deepseek_chat_node.py
├── config.json
├── chat_history.json
└── README.md
```

### Dependencies
- Python 3.6+
- requests library
- ComfyUI environment

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built for ComfyUI
- Powered by DeepSeek's API
- Inspired by community needs for AI integration in visual workflows
