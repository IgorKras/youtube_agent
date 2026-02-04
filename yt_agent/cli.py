import argparse
import logging
import sys
from .config import load_config
from .review_agent import ReviewAgent

def main():
    parser = argparse.ArgumentParser(description="YouTube Telegram Review Agent")
    parser.add_argument("--config", required=True, help="Path to the configuration YAML file")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument("--bot", action="store_true", help="Run in interactive bot mode (listens for Telegram commands)")
    
    args = parser.parse_args()

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger(__name__)

    try:
        logger.info(f"Loading config from {args.config}")
        config = load_config(args.config)
        
        agent = ReviewAgent(config)
        
        if args.bot:
            # Run in interactive bot mode
            logger.info("Starting in interactive bot mode...")
            logger.info("The agent will listen for Telegram commands.")
            logger.info("Send /review to your bot to trigger a review.")
            logger.info("Press Ctrl+C to stop.")
            agent.start_bot_mode()
        else:
            # Run once and exit
            agent.run_review()
        
    except KeyboardInterrupt:
        logger.info("Stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
