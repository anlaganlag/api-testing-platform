import os
import sys
import time
import argparse
import logging
from pathlib import Path

# 添加src目录到Python路径
src_path = Path(__file__).parent / 'src'
sys.path.append(str(src_path))

# 导入修复后的生成器
from enhanced_book_generator_fixed import EnhancedBookGenerator

def setup_logging():
    """设置日志记录"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(f"logs/test_fixed_{int(time.time())}.log", encoding='utf-8')
        ]
    )
    return logging.getLogger("test_fixed")

def test_single_section(generator, logger):
    """测试单个章节的生成"""
    logger.info("测试单个章节生成...")
    
    # 测试数据
    module = "财富管理基础"
    topic = "财富管理概述"
    outline_point = "财富管理的定义与本质"
    description = "解释财富管理的基本概念和核心本质"
    
    # 生成内容
    content = generator.generate_section_content(module, topic, outline_point, description)
    
    if content:
        logger.info("✅ 章节生成成功!")
        logger.info(f"生成内容长度: {len(content)} 字符")
        logger.info(f"内容预览: {content[:100]}...")
        return True
    else:
        logger.error("❌ 章节生成失败!")
        return False

def test_api_providers(generator, logger):
    """测试所有可用的API提供商"""
    logger.info("测试所有API提供商...")
    
    success_count = 0
    for provider in generator.available_providers:
        logger.info(f"测试提供商: {provider}")
        
        # 测试数据
        prompt = f"请用一句话介绍财富管理的重要性。提供商: {provider}"
        
        # 直接使用单一提供商调用
        content = generator._make_single_provider_call(provider, prompt, 100)
        
        if content:
            logger.info(f"✅ {provider} 调用成功!")
            logger.info(f"响应: {content}")
            success_count += 1
        else:
            logger.error(f"❌ {provider} 调用失败!")
    
    logger.info(f"API提供商测试完成: {success_count}/{len(generator.available_providers)} 成功")
    return success_count > 0

def test_parallel_calls(generator, logger):
    """测试并行API调用"""
    logger.info("测试并行API调用...")
    
    # 测试数据
    prompt = "请用一句话描述什么是财富管理。"
    
    # 强制使用并行调用
    old_setting = generator.use_all_providers
    generator.use_all_providers = True
    
    start_time = time.time()
    content = generator._make_api_call(prompt, 100)
    elapsed_time = time.time() - start_time
    
    # 恢复设置
    generator.use_all_providers = old_setting
    
    if content:
        logger.info(f"✅ 并行API调用成功! 耗时: {elapsed_time:.2f}秒")
        logger.info(f"响应: {content}")
        return True
    else:
        logger.error("❌ 并行API调用失败!")
        return False

def test_sample_chapter(generator, logger, chapter_index=0):
    """测试样本章节生成"""
    logger.info(f"测试样本章节生成 (索引: {chapter_index})...")
    
    result = generator.generate_sample_chapter(chapter_index)
    
    if result:
        logger.info("✅ 样本章节生成成功!")
        return True
    else:
        logger.error("❌ 样本章节生成失败!")
        return False

def main():
    parser = argparse.ArgumentParser(description="测试修复后的书籍生成器")
    parser.add_argument("--excel", "-e", default="data/book_outline.xlsx", help="Excel大纲文件路径")
    parser.add_argument("--provider", "-p", choices=["deepseek", "gemini", "openrouter", "siliconflow", "ark", "dashscope", "all"], 
                        default="all", help="要使用的API提供商 (默认: all)")
    parser.add_argument("--test", "-t", choices=["section", "providers", "parallel", "chapter", "all"],
                        default="all", help="要运行的测试类型")
    parser.add_argument("--chapter", "-c", type=int, default=0, help="要生成的样本章节索引")
    
    args = parser.parse_args()
    logger = setup_logging()
    
    try:
        logger.info("初始化修复后的书籍生成器...")
        generator = EnhancedBookGenerator(args.excel, provider=args.provider, max_workers=2)
        
        if args.test == "section" or args.test == "all":
            test_single_section(generator, logger)
        
        if args.test == "providers" or args.test == "all":
            test_api_providers(generator, logger)
        
        if args.test == "parallel" or args.test == "all":
            test_parallel_calls(generator, logger)
        
        if args.test == "chapter" or args.test == "all":
            test_sample_chapter(generator, logger, args.chapter)
        
        logger.info("测试完成!")
        
    except Exception as e:
        logger.error(f"测试过程中发生错误: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())